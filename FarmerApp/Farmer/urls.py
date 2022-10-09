from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('info/', views.ExtractInfoView.as_view(), name='info'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('info_auth/', views.ExtractInfoViewWithAuth.as_view(), name='info_auth'),
    path('upload_auth/', views.UploadViewWithAuth.as_view(), name='upload_auth'),
    path('token-auth/', obtain_auth_token, name='api_token_auth'),

]
