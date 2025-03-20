from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    HyperlinkedIdentityField,
)
from rest_framework.fields import CharField, JSONField
from .models import Dataset, Item


class TagSerializer(Serializer):
    name = CharField(source="name")


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class DatasetListSerializer(ModelSerializer):
    tags = TagSerializer(many=True, allow_null=True, required=False)
    link = HyperlinkedIdentityField(view_name="dataset-detail")
    class Meta:
        model = Dataset
        fields = ("id", "tags","link", "name", "description", "url", "images", "pdfs", "formulas", "paragraphs")

class DatasetDetailSerializer(ModelSerializer):
    tags = TagSerializer(many=True, allow_null=True, required=False)
    class Meta:
        model = Dataset
        fields = "__all__"

class FlowRequestSerializer(Serializer):
    flow_name = CharField()
    parameters = JSONField()