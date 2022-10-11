from urllib.parse import urlsplit

import requests
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .functions import save_farmer, extract_info, code_to_lang
from .serializer import UploadSerializer


def create_user(request):
    if request.method == "POST":
        user = User.objects.create(username=request.POST.get("username"))
        user.set_password(request.POST.get("password"))
        user.save()
        Token.objects.create(user=user)
        return render(request, "after_create_user.html")

    return render(request, "create_user.html")


def info_view(request, lang_id):
    split_url = urlsplit(request.build_absolute_uri())
    response = requests.get(f"{split_url.scheme}://{split_url.netloc}/info/?lang={lang_id}").json()
    return render(request, "info.html", {"farmer_data_list": response, "lang": code_to_lang[lang_id]})


def upload_view(request):
    if request.method == "POST":
        split_url = urlsplit(request.build_absolute_uri())
        requests.post(f"{split_url.scheme}://{split_url.netloc}/upload/",
                      files={"file_uploaded": request.FILES.get('file_uploaded')})
        return render(request, "after_upload.html", {"message": "Farmer Data Successfully Saved"})
    return render(request, "upload.html")


def info_view_auth(request, lang_id):
    token = Token.objects.get(user=request.user)
    split_url = urlsplit(request.build_absolute_uri())
    response = requests.get(f"{split_url.scheme}://{split_url.netloc}/info-auth/?lang={lang_id}",
                            headers={"Authorization": f"Token {token}"}).json()
    return render(request, "info.html", {"farmer_data_list": response, "lang": code_to_lang[lang_id]})


def upload_view_auth(request):
    token = Token.objects.get(user=request.user)
    if request.method == "POST":
        split_url = urlsplit(request.build_absolute_uri())
        requests.post(f"{split_url.scheme}://{split_url.netloc}/upload-auth/",
                      files={"file_uploaded": request.FILES.get('file_uploaded')},
                      headers={"Authorization": f"Token {token}"})
        return render(request, "after_upload.html", {"message": "Farmer Data Successfully Saved"})
    return render(request, "upload.html")


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
        save_farmer(file=request.FILES.get('file_uploaded'))

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
