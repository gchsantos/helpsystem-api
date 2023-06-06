from rest_framework import serializers
from users.models import Customer, Seller


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('username', 'password', 'email', 'cpf', 'gender',
                  'birth', 'is_superuser', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Customer(**validated_data)
        user.set_password(password)
        user.is_staff, user.is_superuser = (
            True, True) if validated_data.pop('is_superuser') else (
            False, False)
        user.save()
        return user


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ('username', 'password', 'email', 'cpf', 'gender',
                  'birth', 'is_superuser', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Seller(**validated_data)
        user.set_password(password)
        user.is_staff, user.is_superuser = (
            True, True) if validated_data.pop('is_superuser') else (
            False, False)
        user.save()
        return user
