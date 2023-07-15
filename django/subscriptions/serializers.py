from django.contrib.auth.models import User
from rest_framework import serializers
from subscriptions.models import StripeCustomer, StripeProduct


class StripeCustomerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = StripeCustomer
        fields = ['user', 'customer_id', 'subscription_id']


class StripeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeProduct
        fields = ['name', 'product_id', 'amount', 'description']