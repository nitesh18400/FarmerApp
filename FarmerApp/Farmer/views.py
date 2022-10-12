from urllib.parse import urlsplit

import requests
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .functions import save_farmer, extract_info, code_to_lang
from .serializer import UploadSerializer, CreateUserSerializer


# Miscellaneous Views
def create_user(request):
    if request.method == "POST":
        # check a username is available or not
        if User.objects.filter(username=request.POST.get("username")).exists():
            return render(request, "create_user.html", {"message": "*Username Not available"})

        # User Creation
        user = User.objects.create(username=request.POST.get("username"))
        user.set_password(request.POST.get("password"))
        user.save()

        # Token Creation
        Token.objects.create(user=user)

        return render(request, "after_create_user.html")

    return render(request, "create_user.html")


class CreateUser(APIView):
    # Input Validation (File Check)
    serializer_class = CreateUserSerializer

    def get(self, request):
        # Sending Message After Hit
        return Response("Enter Details to create new user")

    def post(self, request):
        # check a username is available or not
        if User.objects.filter(username=request.POST.get("username")).exists():
            error_response = {"message": "Username Not Available"}
            final_response = Response(error_response)
            final_response.status_code = 400  # Setting Response Code To Bad Request

            return final_response

        # User Creation
        user = User.objects.create(username=request.POST.get("username"))
        user.set_password(request.POST.get("password"))
        user.save()

        # Token Creation
        Token.objects.create(user=user)

        return Response({"status": True, "message": "User Created"})


# Without Auth Views

# HTML Views

def info_view(request, lang_id):
    # Get Base Url For API Hit
    split_url = urlsplit(request.build_absolute_uri())
    # API Hit Using requests Module
    response = requests.get(f"{split_url.scheme}://{split_url.netloc}/info/?lang={lang_id}").json()

    return render(request, "info.html", {"farmer_data_list": response, "lang": code_to_lang[lang_id]})


def upload_view(request):
    if request.method == "POST":
        # Get Base Url For API Hit
        split_url = urlsplit(request.build_absolute_uri())
        # API Hit Using requests Module
        requests.post(f"{split_url.scheme}://{split_url.netloc}/upload/",
                      files={"file_uploaded": request.FILES.get('file_uploaded')})

        return render(request, "after_upload.html", {"message": "Farmer Data Successfully Saved"})

    return render(request, "upload.html")


# API View

class UploadView(APIView):
    serializer_class = UploadSerializer

    def get(self, request):
        # CSV FILE Upload Message
        return Response("Please Upload CSV File")

    def post(self, request):
        # Save Farmer Function Call for saving and validation Check
        save_farmer(file=request.FILES.get('file_uploaded'))

        return Response({"status": True, "message": "Farmer Data Saved"})  # Post API Response


class ExtractInfoView(APIView):

    # No Authentication Check
    def get(self, request):
        # Calling Info Extraction Function which can Extract Info In Different Language
        response = extract_info(request)

        if response["status"] == 400:
            # Validation Error Handled
            error_response = {"message": response["message"]}
            final_response = Response(error_response)
            final_response.status_code = 400  # Setting Response Code To Bad Request

            return final_response

        return Response({"message": response["message"]}, status=response["status"])


# With Auth Views

# HTML View
def info_view_auth(request, lang_id):
    # Check if Current user is Logged in or Not
    if not request.user.is_authenticated:
        return render(request, "not_logged_in.html")

    # Get Token For Authorization
    token = Token.objects.get(user=request.user)
    # Get Base Url For API Hit
    split_url = urlsplit(request.build_absolute_uri())
    # API Hit with Authorization Header
    response = requests.get(f"{split_url.scheme}://{split_url.netloc}/info-auth/?lang={lang_id}",
                            headers={"Authorization": f"Token {token}"}).json()

    return render(request, "info.html", {"farmer_data_list": response, "lang": code_to_lang[lang_id]})


def upload_view_auth(request):
    # Check if Current user is Logged in or Not
    if not request.user.is_authenticated:
        return render(request, "not_logged_in.html")

    # Get Token For Authorization
    token = Token.objects.get(user=request.user)

    if request.method == "POST":
        # Get Base Url For API Hit
        split_url = urlsplit(request.build_absolute_uri())
        # API Hit with Authorization Header
        requests.post(f"{split_url.scheme}://{split_url.netloc}/upload-auth/",
                      files={"file_uploaded": request.FILES.get('file_uploaded')},
                      headers={"Authorization": f"Token {token}"})

        return render(request, "after_upload.html", {"message": "Farmer Data Successfully Saved"})

    return render(request, "upload.html")


# API View


class UploadViewWithAuth(APIView):
    # Authentication Check (Weather Logged in or using Token)
    permission_classes = (IsAuthenticated,)
    # Input Validation (File Check)
    serializer_class = UploadSerializer

    def get(self, request):
        # Sending Message After Hit
        return Response("Please Upload CSV File")

    def post(self, request):
        # Save Farmer Function Call for saving and validation Check
        save_farmer(file=request.FILES.get('file_uploaded'))

        return Response({"status": True, "message": "Farmer Data Saved"})


class ExtractInfoViewWithAuth(APIView):
    # Authentication Check (Weather Logged in or using Token)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        response = extract_info(request)

        if response["status"] == 400:
            # Setting Error Info and Response Status Code to 400
            final_response = Response({"message": response["message"]})
            final_response.status_code = 400
            return final_response

        return Response({"message": response["message"]}, status=response["status"])
