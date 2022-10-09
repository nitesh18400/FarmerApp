from rest_framework.serializers import Serializer, FileField


class UploadSerializer(Serializer):
    file_uploaded = FileField(required=True)

    class Meta:
        fields = ['file_uploaded']
