from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import StripeCustomer, StripeProduct, Snippet, Domain, Scan


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'url', 'username', 'email', 'groups']


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 
                #   'highlight', 
                  'owner', 'title', 'code', 'linenos', 'language', 'style']


class StripeCustomerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = StripeCustomer
        fields = ['user', 'customer_id', 'subscription_id']


class StripeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeProduct
        fields = ['name', 'product_id', 'amount', 'description']


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['user', 'name', 'ip_address', 'port', 'last_scan']


class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = ['user', 'domain', 'name', 'last_scan']