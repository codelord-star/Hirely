from django.shortcuts import render
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from accounts.models import ProviderProfile

from .serializers import RegisterSerializer, CustomerProfileSerializer, ProviderProfileSerializer

# Create your views here.
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "User registered successfully."},
            status=status.HTTP_201_CREATED
        )
    
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def my_customer_profile(request):
    profile = request.user.customerprofile

    if request.method == 'GET':
        serializer = CustomerProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PATCH':
        serializer = CustomerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProviderProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.provider_profile
        except ProviderProfile.DoesNotExist:
            return Response(
                {"error": "Provider profile not found."},
                status=404
            )

        serializer = ProviderProfileSerializer(profile)
        return Response(serializer.data)

    
    def patch(self, request):
        try:
            profile = request.user.provider_profile
        except ProviderProfile.DoesNotExist:
            return Response(
                {"error": "Provider profile not found."},
                status=404
            )

        serializer = ProviderProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=400
        )


class BecomeProviderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user

        if user.is_provider or ProviderProfile.objects.filter(user=user).exists():
            return Response(
                {"error": "You are already a provider or have a provider profile."},
                status=400
            )
        
        serializer = ProviderProfileSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=400
            )

        
        with transaction.atomic():
            profile = serializer.save(user=user)

            user.is_provider = True
            user.save()

        return Response(
            {
                "message": "You are now a provider.",
                "profile": ProviderProfileSerializer(profile).data
            },
            status=201
        )



class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_provider:
            return Response({"message": "You are a provider."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You are not a provider."}, status=status.HTTP_403_FORBIDDEN)

