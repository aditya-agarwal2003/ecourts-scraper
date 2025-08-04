from django.urls import path
from . import views

urlpatterns = [
    path("", views.case_form, name="case_form"),
]