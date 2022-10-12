from rest_framework.serializers import Serializer, FileField, CharField


class UploadSerializer(Serializer):
    file_uploaded = FileField(required=True)

    class Meta:
        fields = ["file_uploaded"]


class CreateUserSerializer(Serializer):
    username = CharField(max_length=128, write_only=True, required=True)
    password = CharField(max_length=128, write_only=True, required=True)

    class Meta:
        feilds = ["username", "password"]
