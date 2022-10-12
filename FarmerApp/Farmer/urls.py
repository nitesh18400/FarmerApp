from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('create-user/', views.CreateUser.as_view(), name='create-user'),
    path('create-user-view/', views.create_user, name='create-user-view'),
    path('info/', views.ExtractInfoView.as_view(), name='info'),
    path('info-auth/', views.ExtractInfoViewWithAuth.as_view(), name='info-auth'),
    path('info-view/<str:lang_id>', views.info_view, name='info-view'),
    path('info-view-auth/<str:lang_id>', views.info_view_auth, name='info-view-auth'),
    path('token-auth/', obtain_auth_token, name='token-auth'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('upload-auth/', views.UploadViewWithAuth.as_view(), name='upload-auth'),
    path('upload-view/', views.upload_view, name='upload-view'),
    path('upload-view-auth/', views.upload_view_auth, name='upload-view-auth'),
]
