from rest_framework import serializers
from .models import CommonUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonUser
        fields = ('username', 'password', 'email', 'cpf', 'gender','birth', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CommonUser(**validated_data)
        user.set_password(password)
        user.is_staff, user.is_superuser = (True, True) if validated_data.pop('is_superuser') else (False, False)
        user.save()
        return user