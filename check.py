class PublicServiceView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        category_id = request.query_params.get('category')
        provider_county = request.query_params.get('provider_county')
        provider_town = request.query_params.get('provider_town')

        services = Service.objects.filter(is_available=True)

        if category_id:
            services = services.filter(category_id=category_id)

        if provider_county:
            services = services.filter(provider__county=provider_county)

        if provider_town:
            services = services.filter(provider__town=provider_town)

        serializer = PublicServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)