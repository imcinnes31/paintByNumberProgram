from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/upload", views.upload, name="upload"),
    path("/test", views.test, name="test"),
    path("/paintTest", views.paintTest, name="paintTest"),
]