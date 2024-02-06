from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.serializers import JWTSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api import models
from accounts import models as account_models


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = account_models.Subscription
        fields = ['user', 'client_reference_id', 'subscription_type', 'subscription_active', 'period_start', 
                  'period_end', 'previous_subscription_type', 'cancel_at', 'cancel_at_period_end', 'customer_id']
        read_only_fields = ['user', 'client_reference_id', 'subscription_type']


class EmailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = account_models.EmailAddress
        fields = ['user', 'email', 'verified', 'created', 'verification_sent', 'reset_sent']
        read_only_fields = ['id', 'user', 'verified', 'created', 'verification_sent', 'reset_sent']


class UserSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer()
    emails = EmailAddressSerializer(many=True)

    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'subscription', 'emails']


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Domain
        fields = ['id', 'user', 'name', 'ip_address', 'port', 'last_scan', 'created', 'modified']
        read_only_fields = ['id', 'user', 'last_scan', 'created', 'modified']


class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Scan
        fields = ['id', 'user', 'domain', 'uuid', 'output']
        read_only_fields = ['id', 'user', 'domain', 'uuid', 'output']


class ServiceScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Scan
        fields = ['id', 'user', 'domain', 'uuid', 'output']


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Agent
        fields = ['name', 'api_key', 'last_seen']


class ServiceAgentSerializer(serializers.ModelSerializer):
    domains = DomainSerializer(many=True)

    class Meta:
        model = models.Agent
        fields = ['user', 'name', 'api_key', 'last_seen', 'domains']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email']
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
        )
        
        user.set_password(validated_data['password'])
        user.save()

        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    class Meta:
        model = User


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = account_models.EmailAddress


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    class Meta:
        model = User


class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField(required=True)

    class Meta:
        model = account_models.EmailAddress


class CustomJWTSerializer(JWTSerializer):
    user = UserSerializer()
