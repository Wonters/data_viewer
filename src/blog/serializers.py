from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.fields import CharField
from .models import Dataset, Item, Tag

class TagSerializer(Serializer):
    name = CharField(source='name')


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class DatasetSerializer(ModelSerializer):
    tags = TagSerializer(many=True, allow_null=True, required=False)
    class Meta:
        model = Dataset
        fields = '__all__'