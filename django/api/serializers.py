from django.contrib.auth.models import Group, User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.models import (
    # StripeCustomer, 
    StripeProduct, 
    Domain, 
    Scan
)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name',]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


# class StripeCustomerSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.username')

#     class Meta:
#         model = StripeCustomer
#         fields = ['id', 'user', 'customer_id', 'subscription_id']


class StripeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeProduct
        fields = ['id', 'name', 'product_id', 'amount', 'description']


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['id', 'user', 'name', 'ip_address', 'port', 'last_scan', 'created', 'modified']
        read_only_fields = ['user']


class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = ['id', 'user', 'domain', 'uuid', 'last_scan']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField( required=True, validators=[UniqueValidator(queryset=User.objects.all())] )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
        user.set_password(validated_data['password'])
        user.save()

        return user