# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta
from rest_framework import serializers
from django.contrib.auth import get_user_model

from Shop.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, data):
        """
        验证手机号码
        :param data:
        :return:
        """
        if User.objects.filter(mobile=data).exists():
            raise serializers.ValidationError("用户已经存在")

        if not re.match(REGEX_MOBILE, data):
            raise serializers.ValidationError("手机号码非法")

        one_minute_ago = datetime.now() - timedelta(minutes=1)
        if VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=data).exists():
            raise serializers.ValidationError("距离上一次发送未超过一分钟")

        return data
