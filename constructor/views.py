import json
import random

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, viewsets, status
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView

from site_constructor.settings import EMAIL_HOST_USER
from .serializers import GreetSerializer, RegisterSerializer, SampleSerializer, ImageSerializer, SampleStateSerializer
from .models import SampleUser, Sample, Image
from django.contrib.auth.models import User

signer = TimestampSigner()

def send_verification_code(email):
    code = f"{random.randint(100000, 999999)}"  # 6-значный код
    cache.set(f'verify_code_{email}', code, timeout=300)  # 5 минут

    send_mail(
        subject="Ваш код подтверждения",
        message=f"Ваш код подтверждения: {code}",
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )

def verify_code(email, input_code):
    saved_code = cache.get(f'verify_code_{email}')
    if saved_code and input_code == saved_code:
        cache.delete(f'verify_code_{email}')
        return True
    return False

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
            send_verification_code(request.data['email'])
            cache.set(request.data['email'], json.dumps(request.data), timeout=300)
            return Response({
                "user": {
                    "username": request.data['username'],
                    "email": request.data['email']
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        if not email or not code:
            return Response({"error": "Email and code required"}, status=400)

        if verify_code(email, code):
            data = json.loads(cache.get(email))
            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({"message": "Email подтверждён",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Неверный или просроченный код"}, status=400)


# class AuthView(APIView):
#     def get(self, request):
#         serializer = RegisterSerializer(data=request.data)


class SampleView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def post(self, request):
        user_id = request.user.id
        serializer = SampleSerializer(data=request.data.dict() | {"user_id": user_id})
        if serializer.is_valid():
            sample = serializer.save()
            return Response({
                "status": "ok",
                "id": sample.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        path = request.path
        user = request.user
        user_id = request.user.id
        sampleUser = SampleUser.objects.filter(user_id=user.id, sample=request.data["id"])
        if not sampleUser:
            return Response(data={'Not allowed user'}, status=status.HTTP_401_UNAUTHORIZED)
        sample = Sample.objects.get(id=request.data["id"])
        if sample.state == 'open' and sample.is_template == True:
            return Response(data={'Not allowed user'}, status=status.HTTP_401_UNAUTHORIZED)
        if 'state' in path:
            serializer = SampleStateSerializer(data=request.data, instance=sample)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "ok",
                    "id": sample.id
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = SampleSerializer(data=request.data.dict() | {"user_id": user_id}, instance=sample)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "ok",
                "id": sample.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id = None):
        if id:
            # user = request.user
            # sampleUser = SampleUser.objects.filter(user_id=user.id, sample=id)
            # if not sampleUser:
            #     return Response(data={'Not allowed user'}, status=status.HTTP_401_UNAUTHORIZED)
            sample = Sample.objects.get(id = id)
            response_data = {
                    "id": sample.id,
                    "name": sample.name,
                    "image": sample.image.url if sample.image and hasattr(sample.image, 'url') else None,
                    "state": "temp" if sample.is_template else sample.state,
                    "sample_data": sample.data
                }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            user = request.user
            samples = Sample.objects.filter(sampleuser__user_id=user.id)
            open_templates = Sample.objects.filter(state='open', is_template=True)
            response_data = [
                {
                    "id": sample.id,
                    "name": sample.name,
                    "image": sample.image.url if sample.image and hasattr(sample.image, 'url') else None,
                    "state": "temp" if sample.is_template else sample.state,
                }
                for sample in sorted(samples | open_templates, key = lambda x: x.id)
            ]
            return Response(response_data, status=status.HTTP_200_OK)

class SamplesView(APIView):
    def get(self, request):
        samples = Sample.objects.filter(state='open', is_template=False).order_by("id").all()
        response_data = [
            {
                "id": sample.id,
                "name": sample.name,
                "image": sample.image.url if sample.image and hasattr(sample.image, 'url') else None,
                "state": "temp" if sample.is_template else sample.state
            }
            for sample in samples
        ]
        return Response(response_data, status=status.HTTP_200_OK)

class ImageView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.save()
            return Response(data={
                "image": image.image.url
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)