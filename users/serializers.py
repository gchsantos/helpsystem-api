from rest_framework import serializers
from users.models import Customer, Seller, Phone, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('city',)


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('number',)


class CustomerSerializer(serializers.ModelSerializer):
    phone = PhoneSerializer(required=False)
    address = AddressSerializer(required=False)

    class Meta:
        model = Customer
        fields = ('username', 'password', 'email', 'cpf', 'gender', 'birth',
                  'first_name', 'last_name', 'phone', 'address', 'common_id')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        phone = validated_data.pop('phone', None)
        address = validated_data.pop('address', None)

        user = Customer(**validated_data)
        user.set_password(password)
        user.is_staff, user.is_superuser = (False, False)
        user.save()

        if phone:
            Phone.objects.create(user=user, **phone)

        if address:
            Address.objects.create(user=user, **address)

        return user


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ('username', 'password', 'email', 'cpf', 'gender', 'birth',
                  'is_superuser', 'first_name', 'last_name', 'common_id')
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
