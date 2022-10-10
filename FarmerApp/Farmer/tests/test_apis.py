import csv

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class FarmerApiTestCase(TestCase):
    def setUp(self):
        return

    def test_info_access(self):
        response1 = self.client.get("/info/?lang=en")
        response2 = self.client.get("/info/?lang=hi")
        response3 = self.client.get("/info/?lang=mr")
        response4 = self.client.get("/info/?lang=te")
        response5 = self.client.get("/info/?lang=pa")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert response4.status_code == 200
        assert response5.status_code == 200

    def test_info_access_with_wrong_input(self):
        response1 = self.client.get("/info/?lang=er")
        response2 = self.client.get("/info/?lang")
        response3 = self.client.get("/info/")
        assert response1.status_code == 400
        assert response2.status_code == 400
        assert response3.status_code == 400

    def test_upload_access(self):
        with open("test.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(["phone_number", "farmer_name", "state_name", "district_name", "village_name"])
            writer.writerow(["999999999", "Pandey", "Maharashtra", "Wardha", "Deoli"])

        # open file in read mode
        data = open('test.csv', "rb")
        file = SimpleUploadedFile(content=data.read(), name=data.name, content_type='multipart/form-data')

        response = self.client.post("/upload/", {"file_uploaded": file}, format="multipart")
        file.close()

        assert response.status_code == 200

    def test_info_access_with_auth_without_token(self):
        response = self.client.get("/info_auth/?lang")
        assert response.status_code == 401

    def test_upload_access_with_auth_without_token(self):
        response = self.client.get("/upload_auth/")
        assert response.status_code == 401


class FarmerApiAuthTestCase(APITestCase):

    def setUp(self):
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        self.token = Token.objects.create(user=user)

    def test_login(self):
        url = '/token-auth/'
        data = {'username': 'test', 'password': 'test'}
        response = self.client.post(url, data, format='json')
        key = response.json()['token']

        assert key == self.token.key

    def test_info_access_with_auth_with_token(self):
        response = self.client.post("/token-auth/", {'username': 'test', 'password': 'test'}, format='json')

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.json()['token']}")
        response1 = self.client.get("/info_auth/?lang=en")
        response2 = self.client.get("/info_auth/?lang=er")
        response3 = self.client.get("/info_auth/")

        assert response1.status_code == 200
        assert response2.status_code == 400
        assert response3.status_code == 400

    def test_upload_access_with_auth_with_token(self):
        response = self.client.post("/token-auth/", {'username': 'test', 'password': 'test'}, format='json')

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.json()['token']}")

        with open("test.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(["phone_number", "farmer_name", "state_name", "district_name", "village_name"])
            writer.writerow(["999999999", "Pandey", "Maharashtra", "Wardha", "Deoli"])

        # open file in read mode
        data = open('test.csv', "rb")
        file = SimpleUploadedFile(content=data.read(), name=data.name, content_type='multipart/form-data')

        response = self.client.post("/upload_auth/", {"file_uploaded": file}, format="multipart")
        file.close()

        assert response.status_code == 200
