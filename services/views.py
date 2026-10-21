from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from services.serializers import ServiceSerializer

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_service(request):
    if not hasattr(request.user, 'provider_profile'):
        return Response(
            {"error": "You do not have a provider profile."},
            status=status.HTTP_403_FORBIDDEN
        )

    provider = request.user.provider_profile

    serializer = ServiceSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(provider=provider)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    else:
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

