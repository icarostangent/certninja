<<<<<<< HEAD
from django.contrib.auth.models import User
from rest_framework import generics, permissions, mixins, viewsets
from rest_framework.response import Response
from api.permissions import IsOwner
from api.serializers import UserSerializer, RegisterSerializer, LoginSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    # mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner]
=======
>>>>>>> 2956e35 (something)
