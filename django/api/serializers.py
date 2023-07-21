from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import StripeCustomer, StripeProduct, Domain, Scan


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups']


class StripeCustomerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = StripeCustomer
        fields = ['id', 'user', 'customer_id', 'subscription_id']


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