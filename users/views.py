from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserRegisterSerializer


class UserRegistrationView(APIView):

    permission_classes = [AllowAny]

    def post(self):
        serializer = UserRegisterSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        user = User(
            **serializer.validated_data
        )
        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response(status=204)  # registered

