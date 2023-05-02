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
    "job_assessment_id": {
      "type": "string"
    },
    "batch_name": {
      "type": "string"
    },
    "file": {
        "data_type": "file",
        "display_name": "File",
        "uid": "file",
        "extensions": [],
        "field_metadata": {
            "description": "",
            "rich_text_type": "standard"
        },
        "multiple": False,
        "mandatory": False,
        "unique": False
    },

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
    "job_assessment_id",
    "batch_name",
    "file",
    "uploaded_by",
    "uploaded_by_id",
    "processed",
  ],
  "additionalProperties": False
}

