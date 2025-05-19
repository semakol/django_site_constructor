from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import GreetSerializer, RegisterSerializer, SampleSerializer
from .models import User



# class UserViewSet(viewsets.ModelViewSet):
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]

    # def get_object(self):
    #     data = generics.get_object_or_404(Data, pk=self.kwargs['pk'])
    #     user_profile = Profile.objects.get(user=self.request.user)
    #
    #     if data.profile != user_profile:
    #         raise PermissionDenied("Это не ваша запись.")
    #
    #     return data


class GreetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GreetSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            return Response({"message": f"Hello, {name}!"})
        return Response(serializer.errors, status=400)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": {
                    "username": user.username,
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthView(APIView):
    def get(self, request):
        serializer = RegisterSerializer(data=request.data)


class SampleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SampleSerializer(data=request.data)
        if serializer.is_valid():
            sample = serializer.save()
            return Response({
                "status": "ok"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        pass