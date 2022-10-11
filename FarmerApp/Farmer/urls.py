from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('create-user/', views.create_user, name='create-user'),
    path('info-view/<str:lang_id>', views.info_view, name='info-view'),
    path('upload-view/', views.upload_view, name='upload-view'),
    path('info-view-auth/<str:lang_id>', views.info_view_auth, name='info-view-auth'),
    path('upload-view-auth/', views.upload_view_auth, name='upload-view-auth'),
    path('info/', views.ExtractInfoView.as_view(), name='info'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('info-auth/', views.ExtractInfoViewWithAuth.as_view(), name='info-auth'),
    path('upload-auth/', views.UploadViewWithAuth.as_view(), name='upload-auth'),
    path('token-auth/', obtain_auth_token, name='token-auth'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

]
