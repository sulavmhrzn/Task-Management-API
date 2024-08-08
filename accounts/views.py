from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import CreateUserSerializer, UserSerializer
from common.envelope import envelope

from .permissions import IsAdminUserOrCreateOnly


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUserOrCreateOnly]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserSerializer
        elif self.request.method == "POST":
            return CreateUserSerializer
        return super().get_serializer_class()


class UserLogoutView(APIView):
    def post(self, request):
        if request.user.is_anonymous:
            return Response(data=envelope("ok", {"data": "logged out"}))
        try:
            request.user.auth_token.delete()
        except Exception as ex:
            # USE LOGGING
            print("EXCEPTION:", ex)
            return Response(
                data=envelope("fail", "Internal server error"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(data=envelope("ok", {"data": "logged out"}))


class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(envelope(status="ok", message={"token": token.key}))
