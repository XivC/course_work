from rest_framework import serializers


class UserRegisterSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(default='', required=False)
    last_name = serializers.CharField(default='', required=False)
