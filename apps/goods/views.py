from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Goods, GoodsCategory
from .serializers import GoodsSerializer, CategorySerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List all goods.
    """
    serializer_class = GoodsSerializer

    def get_queryset(self):
        return Goods.objects.all()


class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:   商品分类列表数据
    retrieve:   获得某个商品的详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
