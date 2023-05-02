from rest_framework import serializers

class BatchSerializer(serializers.Serializer):

    class Meta:
        fields = '__all__'


    def to_representation(self, instance):
        # Serialize the `_id` field to a string
        if '_id' in instance:
            instance["_id"] = str(instance["_id"])

        # Deserialize the instance to a Python dictionary
        job_dict = serializers.JSONField().to_representation(instance)
        # Create a new dictionary without the `id` field
        job_dict.pop("id", None)
        return job_dict