from django.urls import path
from .views import upload_pdf, download_pdf

urlpatterns = [
    path('', upload_pdf, name='upload_pdf'),
    path('download/', download_pdf, name='download_pdf'),
]
