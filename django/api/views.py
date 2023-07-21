import os
import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, mixins, renderers, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from api import models
from api import serializers
from api.permissions import IsOwner, IsOwnerOrReadOnly


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    # mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsOwner]


class StripeCustomerViewSet(ReadOnlyModelViewSet):
    queryset = models.StripeCustomer.objects.all()
    serializer_class = serializers.StripeCustomerSerializer
    permission_classes = [IsOwner]
    lookup_field = 'user'


class StripeProductViewSet(ReadOnlyModelViewSet):
    queryset = models.StripeProduct.objects.all()
    serializer_class = serializers.StripeProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class DomainViewSet(ModelViewSet):
    queryset = models.Domain.objects.all()
    serializer_class = serializers.DomainSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Domain.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ScanViewSet(ReadOnlyModelViewSet):
    queryset = models.Scan.objects.all()
    serializer_class = serializers.ScanSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'domain'

    def get_queryset(self):
        return models.Scan.objects.filter(domain=self.kwargs['pk'], user=self.request.user)


@api_view(['POST'])
def create_payment_intent(request):
    customer = models.StripeCustomer.objects.get(user_id=request.data.get('pk'))
    try:
        payment_intent = stripe.PaymentIntent.create(
            api_key=os.environ.get('STRIPE_SECRET_KEY', 'go get a secret key'),
            customer=customer.customer_id,
            amount=2000,
            currency="usd",
            payment_method_types=["card"],
        )
    except Exception as ex:
        print('exception:')
        print(ex)
        return HttpResponse(status=400)

    return JsonResponse({
        'client_secret': payment_intent.client_secret,
        'publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    print(event)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # client_reference_id = session.get('client_reference_id')
        # stripe_customer_id = session.get('customer')
        # stripe_subscription_id = session.get('subscription')

        # user = User.objects.get(id=client_reference_id)
        # StripeCustomer.objects.create(
        #     user=user,
        #     stripeCustomerId=stripe_customer_id,
        #     stripeSubscriptionId=stripe_subscription_id,
        # )
        # print(user.username + ' just subscribed.')

    return HttpResponse(status=200)
