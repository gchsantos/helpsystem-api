from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

from .serializers import CustomerSerializer, SellerSerializer


class CustomerCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (AllowAny,)


class SellerCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SellerSerializer
    permission_classes = (AllowAny,)
