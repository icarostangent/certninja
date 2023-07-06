from django.contrib import auth
from django.contrib.auth.models import User, Group
from rest_framework import generics, permissions, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from knox.models import AuthToken
from api.serializers import UserSerializer, RegisterSerializer, LoginSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class SignUpAPI(generics.GenericAPIView):
    authentication_classes = [BasicAuthentication]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user)
        return Response({
            "users": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token[1]
        })


class SignInAPI(generics.GenericAPIView):
    # authentication_classes = [BasicAuthentication]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class MainUser(generics.RetrieveAPIView):
  permission_classes = [
      permissions.IsAuthenticated
  ]
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user