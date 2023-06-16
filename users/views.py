from rest_framework import generics, status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from helpsystem_api.messages import ReturnBaseMessage
from users.serializers import CommonUserSerializer, CustomerSerializer, SellerSerializer
from users.models import CommonUser
from users.constants import ErrorMessages


class CustomerCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (AllowAny,)


class SellerCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SellerSerializer
    permission_classes = (AllowAny,)


class CommonUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        try:
            common_user = CommonUser.objects.get(user_ptr=request.user)
        except CommonUser.DoesNotExist:
            return ReturnBaseMessage(
                success=False, detail=ErrorMessages.COMMONUSER_DOES_NOT_EXIST,
                code=status.HTTP_400_BAD_REQUEST).message

        common_user_serialized = CommonUserSerializer(common_user).data
        return ReturnBaseMessage(detail=common_user_serialized).message
