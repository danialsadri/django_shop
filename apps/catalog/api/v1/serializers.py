from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from apps.catalog.models import Category


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        return CategoryListSerializer(obj.get_children(), many=True).data

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'description', 'is_public', 'children']


class CategoryCreateSerializer(serializers.ModelSerializer):
    parent = serializers.IntegerField(required=False)

    def create(self, validated_data):
        parent = validated_data.pop('parent', None)
        if parent is None:
            instance = Category.add_root(**validated_data)
        else:
            parent_node = get_object_or_404(Category, pk=parent)
            instance = parent_node.add_child(**validated_data)
        return instance

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'description', 'is_public', 'parent']


class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'is_public']


CategoryListSerializer.get_children = extend_schema_field(serializers.ListField(child=CategoryListSerializer()))(CategoryListSerializer.get_children)
