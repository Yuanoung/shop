# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
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


class UserRegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4, min_length=4, required=True, label="验证码", write_only=True,
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误",
                                 })
    password = serializers.CharField(label="密码", style={'input_type': 'password'}, write_only=True)
    username = serializers.CharField(label="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message="用户已经存在")])

    # def create(self, validated_data):  # 可以改用signals
    #     user = super(UserRegisterSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        five_minutes_ago = datetime.now() - timedelta(minutes=5)
        last_recodes = VerifyCode.objects.filter(mobile=self.initial_data["username"],
                                                 add_time__gt=five_minutes_ago,
                                                 code=code).order_by("-add_time").first()
        if last_recodes:
            return None
        else:
            raise serializers.ValidationError("验证码错误或过期")

    def validate(self, attrs):
        """
        valadate_field验证后，会执行这个
        :param attrs:
        :return:
        """
        attrs["mobile"] = attrs["username"]
        attrs.pop("code", None)  # 这里已经将code删除了，serializer.data会报错
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")
