from django.contrib.auth.models import User
from rest_framework import serializers
from subscriptions.models import StripeProduct


class StripeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeProduct
        fields = ['name', 'product_id', 'amount', 'description']
