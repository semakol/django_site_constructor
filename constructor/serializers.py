import datetime

from rest_framework import serializers
from .models import Sample, SampleUser, Image
from django.contrib.auth.models import User
from .common import hash_password

class GreetSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    second_name = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'second_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        if validated_data.get('second_name'):
            validated_data['last_name'] = validated_data.pop('second_name')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class SampleSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False, default='')
    sample_data = serializers.CharField(required=False)
    user_id = serializers.IntegerField(required=True)

    class Meta:
        model = Sample
        fields = ['sample_data', 'name', 'state', 'image', 'user_id']

    def create(self, validated_data):
        sample = Sample.objects.create(
            name = validated_data['name'],
            data = validated_data['sample_data'],
            state = validated_data['state'],
            image = validated_data['image'],
            date_create = datetime.datetime.utcnow(),
            date_update = datetime.datetime.utcnow()
        )
        user = User.objects.get(id=validated_data['user_id'])
        sampleUser = SampleUser.objects.create(
            relation = 'creator',
            user_id = user,
            sample = sample
        )
        return sample

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'

    def create(self, validated_data):
        image = Image.objects.create(**validated_data)
        return image


# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, min_length=6)
#
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'role', 'first_name', 'second_name']
#         extra_kwargs = {
#             'first_name': {'required': False},
#             'second_name': {'required': False}
#         }
#
#
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             password_hash=hash_password(validated_data['password']),
#             role=validated_data['role'],
#             first_name=validated_data['first_name'],
#             second_name=validated_data['second_name']
#         )
#         return user