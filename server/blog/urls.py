from django.urls import path, include
from .views import ListDatasetView, DatasetViewSet, LaunchFlowView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("datasets", DatasetViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("view/", ListDatasetView.as_view()),
    path("flow/", LaunchFlowView.as_view())
]
