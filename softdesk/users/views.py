from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from users.serializer import UserSerializer
from rest_framework.permissions import AllowAny


class UserViewSet(ModelViewSet):
    """
    ViewSet for managing users.
    Allows authenticated users to retrieve, update, and delete user accounts.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class RegisterUserView(APIView):
    """
    View for registering new users.
    Allows unauthenticated users to create an account.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        password = data.get('password')

        if not password:
            return Response({"error": "Le mot de passe est requis."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=data.get('username'),
            email=data.get('email'),
            age=data.get('age'),
            can_be_contacted=data.get('can_be_contacted', False),
            can_data_be_shared=data.get('can_data_be_shared', False),
        )
        user.set_password(password)
        user.save()

        return Response({"message": "Utilisateur créé avec succès."}, status=status.HTTP_201_CREATED)
