from random import sample

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
from .models import User, SampleUser, Sample



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

# class ImageViev(APIView):


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
        user_id = request.user.id
        serializer = SampleSerializer(data=request.data | {"user_id": user_id})
        if serializer.is_valid():
            sample = serializer.save()
            return Response({
                "status": "ok"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        pass

    def get(self, request, id = None):
        if id:
            sample = 1
            pass
        else:
            user = request.user
            samples = Sample.objects.filter(sampleuser__user_id=user.id)
            response_data = [
                {
                    "name": sample.name,
                    "image": sample.image.url if sample.image and hasattr(sample.image, 'url') else None,
                    "state": sample.state,
                }
                for sample in samples
            ]
            return Response(response_data, status=status.HTTP_200_OK)
