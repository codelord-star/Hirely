from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.models import ProviderProfile
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
        provider_county = request.query_params.get('provider_county')
        provider_town = request.query_params.get('provider_town')
        pricing_type = request.query_params.get('pricing_type')

        search_query = request.query_params.get('search', '')
        search_terms = search_query.split()

        sort_date = request.query_params.get('sort_date')
        sort_price = request.query_params.get('sort_price')
        valid_date_options = ['newest', 'oldest']
        valid_price_options = ['price_asc', 'price_desc']

        if sort_date and sort_date not in valid_date_options:
            return Response(
                {"error": "Invalid date sorting option."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if sort_price and sort_price not in valid_price_options:
            return Response(
                {"error": "Invalid price sorting option."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if category_id and not category_id.isdigit():
            return Response(
                {"error": "Invalid category ID."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if category_id and not Category.objects.filter(id=category_id).exists():
            return Response(
                {"error": "Category does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        valid_counties = [choice[0] for choice in ProviderProfile.COUNTY_CHOICES]
        if provider_county and provider_county not in valid_counties:
            return Response(
                {"error": "Invalid county."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if provider_town is not None and not provider_town.strip():
            return Response(
                {"error": "Invalid filter."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if provider_town is not None:
            provider_town = provider_town.strip()
        
        valid_pricing_types = [choice[0] for choice in Service.PRICING_TYPE_CHOICES]
        if pricing_type and pricing_type not in valid_pricing_types:
            return Response(
                {"error": "Invalid pricing type."},
                status=status.HTTP_400_BAD_REQUEST
            )

        services = Service.objects.filter(is_available=True)

        if category_id:
            services = services.filter(category_id=category_id)

        if provider_county:
            services = services.filter(provider__county=provider_county)

        if provider_town:
            services = services.filter(provider__town__iexact=provider_town)

        if pricing_type:
            services = services.filter(pricing_type=pricing_type)

        for term in search_terms:
            search_conditions = (
                Q(title__icontains=term) |
                Q(description__icontains=term) |
                Q(provider__business_name__icontains=term) |
                Q(provider__county__icontains=term) |
                Q(provider__town__icontains=term) |
                Q(provider__specific_address__icontains=term)
            )
            services = services.filter(search_conditions)

        ordering = []
        if sort_date is None and sort_price is None:
            ordering.append('-created_at')

        if sort_date == 'newest':
            ordering.append('-created_at')

        elif sort_date == 'oldest':
            ordering.append('created_at')

        if sort_price == 'price_asc':
            ordering.append('price_ksh')
        elif sort_price == 'price_desc':
            ordering.append('-price_ksh')

        services = services.order_by(*ordering)

        serializer = PublicServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PublicServiceDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, service_id):
        service = get_object_or_404(Service, id=service_id, is_available=True)
        serializer = PublicServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)


    