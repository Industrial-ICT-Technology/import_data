from django.urls import path
from . import views

app_name = 'upload'

urlpatterns = [
    path('', views.Import_csv, name="Import_csv"),
]
