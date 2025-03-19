from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListCreateAPIView

from .models import Dataset
from .serializers import DatasetSerializer

class ListCreateDatasetView(ListCreateAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer