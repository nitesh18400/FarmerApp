from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .functions import save_farmer, extract_info
from .serializer import UploadSerializer


class ExtractInfoView(APIView):

    def get(self, request):
        response = extract_info(request)

        if response["status"] == 400:
            final_response = Response({"message": response["message"]})
            final_response.status_code = 400
            return final_response

        return Response({"message": response["message"]}, status=response["status"])


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

        if response["status"] == 400:
            final_response = Response({"message": response["message"]})
            final_response.status_code = 400
            return final_response

        return Response({"message": response["message"]}, status=response["status"])


class UploadView(APIView):
    serializer_class = UploadSerializer

    def get(self, request):
        return Response("Please Upload CSV File")

    def post(self, request):
        save_farmer(file=request.FILES.get('file_uploaded'))

        return Response({"status": True, "message": "Farmer Data Saved"})
