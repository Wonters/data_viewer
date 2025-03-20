from django.views.generic import View
from django.views.generic.list import ListView
from django.http.response import JsonResponse
from rest_framework.viewsets import ModelViewSet
from .tasks import create_dataset
from .models import Dataset
from .serializers import DatasetListSerializer, DatasetDetailSerializer, FlowRequestSerializer


class ListDatasetView(ListView):
    template_name = "blog/blog_list.html"
    queryset = Dataset.objects.all()
    context_object_name = "datasets"


class DatasetViewSet(ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetListSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DatasetDetailSerializer
        return self.serializer_class

class LaunchFlowView(View):

    def post(self, request, *args, **kwargs):
        serializer = FlowRequestSerializer(data=request.data)
        if serializer.is_valid():
            payload = serializer.validated_data
            task  = create_dataset.delay(*payload)
            return JsonResponse({"message": f"Flow {payload['flow_name']}",
                                 "task":task.id})
        return JsonResponse(serializer.errors, status=400)
