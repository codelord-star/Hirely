from django.shortcuts import render, get_object_or_404

from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from services.models import Category, Service
from services.serializers import CategorySerializer, PublicServiceSerializer, ServiceSerializer

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

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_service(request, service_id):
    if not hasattr(request.user, 'provider_profile'):
        return Response(
            {"error": "You do not have a provider profile."},
            status=status.HTTP_403_FORBIDDEN
        )

    provider = request.user.provider_profile

    service = get_object_or_404(provider.services, id=service_id)

    serializer = ServiceSerializer(service, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_services(request):
    if not hasattr(request.user, 'provider_profile'):
        return Response(
            {"error": "You do not have a provider profile."},
            status=status.HTTP_403_FORBIDDEN
        )

    provider = request.user.provider_profile
    services = provider.services.all()
    serializer = ServiceSerializer(services, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_service(request, service_id):
    if not hasattr(request.user, 'provider_profile'):
        return Response(
            {"error": "You do not have a provider profile."},
            status=status.HTTP_403_FORBIDDEN
        )

    provider = request.user.provider_profile
    service = get_object_or_404(provider.services, id=service_id)
    serializer = ServiceSerializer(service)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_service(request, service_id):
    if not hasattr(request.user, 'provider_profile'):
        return Response(
            {"error": "You do not have a provider profile."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    provider = request.user.provider_profile
    service = get_object_or_404(provider.services, id=service_id)

    service.delete()
    return Response(
        status=status.HTTP_204_NO_CONTENT
    )

@api_view(['GET'])
def list_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class PublicServiceView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        category_id = request.query_params.get('category')

        if category_id:
            services = Service.objects.filter(is_available=True, category_id=category_id)
        else:
            services = Service.objects.filter(is_available=True)

        serializer = PublicServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PublicServiceDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, service_id):
        service = get_object_or_404(Service, id=service_id, is_available=True)
        serializer = PublicServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)


    