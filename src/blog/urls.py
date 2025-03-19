from django.urls import path
from .views import ListCreateDatasetView

urlpatterns = [
    path('blog/', ListCreateDatasetView.as_view()),
]