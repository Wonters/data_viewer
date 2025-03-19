from django.urls import path
from .views import ListCreateDatasetView, ListDatasetView

urlpatterns = [
    path("api/", ListCreateDatasetView.as_view()),
    path("view/", ListDatasetView.as_view()),
]
