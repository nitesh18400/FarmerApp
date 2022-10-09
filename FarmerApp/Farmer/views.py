from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .functions import save_farmer, extract_info
from .serializer import UploadSerializer


class ExtractInfoView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        response = extract_info(request)

        return Response(response)


class UploadViewWithAuth(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UploadSerializer

    def get(self, request):
        return Response("Please Upload CSV File")

    def post(self, request):
        save_farmer(request)

        return Response({"status": True, "message": "Farmer Data Saved"})


class ExtractInfoViewWithAuth(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        response = extract_info(request)

        return Response(response)


class UploadView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = UploadSerializer

    def get(self, request):
        return Response("Please Upload CSV File")

    def post(self, request):
        save_farmer(request)

        return Response({"status": True, "message": "Farmer Data Saved"})
