from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import UserSerializer
from common.envelope import envelope


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


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
