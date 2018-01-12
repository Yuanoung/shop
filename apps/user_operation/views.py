from rest_framework import viewsets, mixins

from .models import UserFav
from .serializers import UserFavSerializer


class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    用户收藏功能
    """
    serializer_class = UserFavSerializer
    queryset = UserFav.objects.all()
