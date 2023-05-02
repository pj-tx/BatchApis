from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.validators import FileExtensionValidator
from .serializers import BatchSerializer

from rest_framework.views import APIView

from .schema import BatchSchema
import datetime, pytz

from jsonschema import Draft7Validator, FormatChecker, ValidationError

from pymongo import MongoClient
from bson.objectid import ObjectId

from .db import jdclient, data_db

import json
from urllib.parse import urlencode


import magic
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3',aws_access_key_id="AKIAS6NGRAVA3BO2OIP5",aws_secret_access_key="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",region_name="ap-south-1")


# def validate_file(value):
#     mime = magic.Magic(mime=True)
#     file_type = mime.from_buffer(value.read(1024))
#     file_mime_type = mime.from_file(value)
#     print("Validator Called")
#     print(file_type)

#     if not file_type in ['text/csv', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
#         print("This should run")
#         return Response(data={"status": "failed", "status_code": "400", "error_code": "TA8001", "errors": {"field":"","message":"Invalid File, Only .csv, .xls, .xlsx are allowed"}}, status=404)


class BatchViewSet(viewsets.ViewSet):

    def get(self, request):  
        data = request.data

        query = request.query_params.copy() or {}

        # query['is_deleted'] = False

        if "id" in query:
            query = {"_id" : ObjectId(query.get("id"))}


        assess_collection = data_db("batches") 
        jobs = assess_collection.find(query)

        if jobs.count() > 0:
            serializer = BatchSerializer(jobs, many=True)
            return Response(data=serializer.data, status=201)
        else:
            return Response(data={}, status=200)

    def create(self, request):
        print("Posting Started")

        data = request.data

        data["uploaded_time"] = datetime.datetime.now(tz=pytz.UTC).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        data["processed"] = False
        # Check if the request contains a file
        if 'file' not in request.FILES:
            return Response(data={"status": "failed", "status_code": "400", "error_code": "TA8001", "errors": {"field":"","message":"File Not Found"}}, status=404)

        # Get the file from the request
        file = request.FILES['file']

        # Validate file type
        file_extension_validator = FileExtensionValidator(allowed_extensions=['csv', 'xls', 'xlsx'])
        try:
            file_extension_validator(file)
        except Exception as e:
            print(e)
            return Response(data={"status": "failed", "status_code": "400", "error_code": "TA8001", "errors": {"field":"","message":e}}, status=404)
        
        schema = BatchSchema

        serializer = BatchSerializer(data=data)
        if serializer.is_valid():
            v=Draft7Validator(schema=schema,format_checker=FormatChecker())
            if len(list(v.iter_errors(data)))!=0:
                validation_errors = list(v.iter_errors(data))
                errors=[]
                for error in validation_errors:
                    errors.append({
                        'field': error.path[0] if error.path else '',
                        'message': error.message
                    })
                return Response(data={"status": "failed", "status_code": "400", "error_code": "TA8001", "errors": errors}, status=400)
            else:
                # Upload to s3 here
                # Create S3 key name with format <job_title>_<name>.<extension>
                file_extension = file.name.split('.')[-1]
                # YYYYMMDDHHSS-BatchName-Recruitername
                dt_string = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                s3_key = f"{dt_string}-{data['batch_name']}-{data['uploaded_by']}.{file_extension}".replace(" ", "")

                # Upload file to S3
                s3_bucket = "batchuploadtest"
                try:
                    response = s3.upload_fileobj(file, s3_bucket, s3_key)
                except ClientError as e:
                    print("error occured")
                    print(e)
                    return Response(data={"status": "failed", "status_code": "400", "error_code": "TA8001", "errors": {"field":"","message":e}}, status=404)

                # Create S3 URL
                s3_url = f"https://{s3_bucket}.s3.amazonaws.com/{s3_key}"

                data.pop('file')
                data["s3_url"]= s3_url
                json_data = json.dumps(data)
                jaon_data = json.loads(json_data)


                print(jaon_data)

                # json_data = json.dumps(data)
                # print(json_data)

                collection = data_db("batches")
                result = collection.insert_one(jaon_data)
                response_data = {"status": "passed" ,"message":"Batch Uploaded Successfully" ,'id': str(result.inserted_id)}
                return Response(data=response_data, status=201)
        else:
            return Response(serializer.errors, status=400)
        

class ForiegnFields(APIView):

    def get(self, request):  
        data = request.data

        query = request.query_params.copy() or {}

        if "id" in query:
            query = {"job_id" : str(query.get("id"))}
            assess_collection = data_db("jd_assessments") 
            jobs = assess_collection.find(query)

        else:
            collection = jdclient() 
            jobs = collection.find({"is_deleted": False}, {"_id": 1, "title": 1})

        if jobs.count() > 0:
            serializer = BatchSerializer(jobs, many=True)
            return Response(data=serializer.data, status=201)
        else:
            return Response(data={}, status=200)
