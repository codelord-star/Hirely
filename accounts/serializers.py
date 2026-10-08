from rest_framework import serializers
from .models import User, CustomerProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField(max_length=200)
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password', 'full_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )

        CustomerProfile.objects.create(
                user=user,
                full_name=validated_data['full_name']
            )

        return user
    

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['full_name', 'created_at']
        read_only_fields = ['created_at']
