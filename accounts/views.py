from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer

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




class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_provider:
            return Response({"message": "You are a provider."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "You are not a provider."}, status=status.HTTP_403_FORBIDDEN)

