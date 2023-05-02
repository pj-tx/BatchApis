BatchSchema = {
  "$id": "root",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "uploaded_time": {
      "type": "string",
      "format": "date-time"
    },
    "job_id": {
      "type": "string"
    },
    "job_title": {
      "type": "string"
    },
    "job_assessment": {
      "type": "string"
    },
    "batch_name": {
      "type": "string"
    },
    # "file": {
    #     "type": "object",
    #     "properties": {
    #         "filename": {
    #             "type": "string",
    #             "pattern": "^.*\\.(csv|xlsx|xls)$"
    #         },
    #         "content_type": {
    #             "type": "string",
    #             "pattern": "^application/(csv|xlsx|xls)$"
    #         },
    #         "content": {
    #             "type": "string",
    #             "format": "binary"
    #         }
    #     },
    #     "required": [
    #         "name",
    #         "content"
    #     ]
    # },
    "uploaded_by": {
      "type": "string",
    },
    "uploaded_by_id": {
      "type": "string",
    },
    "processed":{
      "type":"boolean",
      "default":False
    },
  },
  "required": [
    "job_id",
    "job_title",
    "job_assessment",
    "batch_name",
    "file",
    "uploaded_by",
    "uploaded_by_id",
    "processed",
  ],
  "additionalProperties": True
}

