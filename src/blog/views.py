from django.views.generic import TemplateView
from django.views.generic.list import ListView
from rest_framework.generics import ListCreateAPIView

from .models import Dataset
from .serializers import DatasetSerializer

class ListDatasetView(ListView):
    template_name = "blog/blog_list.html"
    queryset = Dataset.objects.all()
    context_object_name = "datasets"


class ListCreateDatasetView(ListCreateAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
