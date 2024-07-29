from rest_framework import viewsets
from rest_framework.exceptions import NotAcceptable
from apps.catalog.models import Category
from .serializers import (
    CategoryRetrieveSerializer, CategoryListSerializer,
    CategoryCreateSerializer, CategoryUpdateSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        if self.action == 'list':
            return Category.objects.filter(depth=1)
        else:
            return Category.objects.all()

    def get_serializer_class(self):
        match self.action:
            case 'retrieve':
                return CategoryRetrieveSerializer
            case 'list':
                return CategoryListSerializer
            case 'create':
                return CategoryCreateSerializer
            case 'update':
                return CategoryUpdateSerializer
            case 'partial_update':
                return CategoryUpdateSerializer
            case 'destroy':
                return CategoryUpdateSerializer
            case _:
                raise NotAcceptable()
