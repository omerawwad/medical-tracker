from rest_framework import serializers
from .models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'password', 'is_active', 'is_staff', 'birth_date', 'phone_number', 'address']
        read_only_fields = ['id', 'is_active', 'is_staff']
        extra_kwargs = {
            'email': {'required': True, 'allow_blank': False},
            'username': {'required': True, 'allow_blank': False},
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
            'name': {'required': False, 'allow_blank': True},
            'birth_date': {'required': False, 'allow_null': True},
            'phone_number': {'required': False, 'allow_blank': True},
            'address': {'required': False, 'allow_blank': True},
            'password': {'write_only': True, 'min_length': 0, 'required': True, 'allow_blank': False}
        }

    def create(self, validated_data):
        # Hash Password
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    