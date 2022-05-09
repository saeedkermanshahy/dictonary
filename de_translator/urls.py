from django.urls import path
from . import views

urlpatterns = [
    path("", views.de_translator, "de_translator"),
]
