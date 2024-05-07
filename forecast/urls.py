from django.urls import path
from . import views

urlpatterns = [
    path("", views.PositionFormView.as_view(), name="position"),
]