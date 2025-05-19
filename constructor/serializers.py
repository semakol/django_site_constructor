import datetime

from rest_framework import serializers
from .models import User, Sample
from .common import hash_password

class GreetSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'first_name', 'second_name']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class SampleSerializer(serializers.ModelSerializer):
    sample_data = serializers.CharField(required=False)

    class Meta:
        model = Sample
        fields = ['sample_data', 'name', 'state']

    def create(self, validated_data):
        sample = Sample.objects.create(
            name = validated_data['name'],
            data = validated_data['sample_data'],
            state = validated_data['state'],
            date_create = datetime.datetime.utcnow(),
            date_update = datetime.datetime.utcnow()
        )
        return sample



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