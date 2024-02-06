import stripe
from datetime import datetime
from django import http
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password 
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, mixins, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from api import exceptions
from api import models
from api import serializers
from api.permissions import IsOwner
from accounts import models as account_models
from accounts.signals import password_reset_signal


class ServiceAgentView(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.ServiceAgentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = models.Agent.objects.get(api_key=request.data['api_key'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ServiceScanView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.ServiceScanSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AgentViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.AgentSerializer

    def get_queryset(self):
        return models.Agent.objects.filter(user=self.request.user)


class EmailAddressViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.EmailAddressSerializer

    def get_queryset(self):
        return account_models.EmailAddress.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionViewSet(ReadOnlyModelViewSet):
    queryset = account_models.Subscription.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.SubscriptionSerializer


class RegisterViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    # mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsOwner]


class DomainViewSet(ModelViewSet):
    serializer_class = serializers.DomainSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Domain.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        subscription = self.request.user.subscription
        if not subscription.subscription_active:
            raise exceptions.SubscriptionInactive
        if self.request.user.domains.count() >= settings.DOMAIN_LIMITS[subscription.subscription_type]:
            raise exceptions.DomainLimitExceeded
        serializer.save(user=self.request.user)


class ScanViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.ScanSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'domain'

    def get_queryset(self):
        return models.Scan.objects.filter(domain=self.kwargs['pk'], user=self.request.user)


@csrf_exempt
def stripe_webhook(request):
    if not settings.STRIPE_SECRET_KEY:
        print('stripe secret key not configured')
    if not settings.STRIPE_WEBHOOK_SECRET:
        print('stripe webhook secret not configured')
    stripe.api_key = settings.STRIPE_SECRET_KEY
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    session = event['data']['object']
    import json
    now = datetime.now().strftime("%m-%d-%H:%M:%S")
    print_str = f"{now} {event['type']}"

    if event['type'] == 'checkout.session.completed':
        print(f'[*] {print_str}')
        with open(f'src/{print_str}.json', 'w') as f:
            json.dump(session, f, indent=4)
        # print(session)
        # check to see if customer exists. if not, create it
        subscription = get_object_or_404(account_models.Subscription, client_reference_id=session['client_reference_id'])
        if not subscription.customer_id:
            print(f"[+] new customer")
            subscription.customer_id = session['customer']
            subscription.save()
        stripe_sub = stripe.Subscription.retrieve(session['subscription'])
        with open(f'src/{now} subscription.json', 'w') as f:
            json.dump(stripe_sub, f, indent=4)
        # fulfill_subscription(stripe_sub) 
        subscription = get_object_or_404(account_models.Subscription, customer_id=stripe_sub['customer'])
        subscription.period_start = datetime.utcfromtimestamp(session['current_period_start'])
        subscription.period_end = datetime.utcfromtimestamp(session['current_period_end'])
        subscription.subscription_type = settings.STRIPE_PRODUCT_IDS[session['items']['data'][0]['plan']['product']]
        subscription.subscription_id = session['id']
        subscription.subscription_active = session['items']['data'][0]['plan']['active']
        subscription.save()

    if event['type'] == 'customer.subscription.created':
        print(f'[*] {print_str}')
        with open(f'src/{print_str}.json', 'w') as f:
            json.dump(session, f, indent=4)
        # print(session)
        subscription = get_object_or_404(account_models.Subscription, customer_id=session['customer'])
        subscription.period_start = datetime.utcfromtimestamp(session['current_period_start'])
        subscription.period_end = datetime.utcfromtimestamp(session['current_period_end'])
        subscription.subscription_type = settings.STRIPE_PRODUCT_IDS[session['items']['data'][0]['plan']['product']]
        subscription.subscription_id = session['id']
        subscription.subscription_active = session['items']['data'][0]['plan']['active']
        subscription.save()

    if event['type'] == 'customer.subscription.updated':
        print(f'[*] {print_str}')
        with open(f'src/{print_str}.json', 'w') as f:
            json.dump(session, f, indent=4)
        # print(session)
        subscription = get_object_or_404(account_models.Subscription, customer_id=session['customer'])
        subscription.period_start = datetime.utcfromtimestamp(session['current_period_start'])
        subscription.period_end = datetime.utcfromtimestamp(session['current_period_end'])
        subscription.subscription_type = settings.STRIPE_PRODUCT_IDS[session['items']['data'][0]['plan']['product']]
        subscription.subscription_active = session['items']['data'][0]['plan']['active']
        # if 'items' in session['previous_attributes']:
        #     subscription.previous_subscription_type = settings.STRIPE_PRODUCT_IDS[session['previous_attributes']['items']['data'][0]['plan']['product']]
        if session['cancel_at_period_end']:
            subscription.cancel_at = datetime.utcfromtimestamp(session['cancel_at'])
        if session['cancellation_details']['reason'] == 'cancellation_requested':
            subscription.cancel_at_period_end = True
            subscription.previous_subscription_type = subscription.subscription_type
            subscription.subscription_type = 'canceled'
        subscription.save()

    if event['type'] == 'customer.updated':
        print(f'[*] {print_str}')
        with open(f'src/{print_str}.json', 'w') as f:
            json.dump(session, f, indent=4)
        customer = get_object_or_404(User, subscription__customer_id=session['id'])
        if customer.email != session['email']:
            customer.email = session['email']
            customer.save()
            match = False
            for email_address in customer.email_addresses.all():
                if email_address.email == session['email']:
                    match = True
            if not match:
                account_models.EmailAddress.objects.create(user=customer, email=session['email'])

    return HttpResponse(status=200)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,])
def get_customer_portal(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    stripe.billing_portal.Configuration.create(
        business_profile={
            "headline": "Cactus Practice partners with Stripe for simplified billing.",
        },
        features={ "invoice_history": { "enabled": True } },
    )

    session = stripe.billing_portal.Session.create(
        customer=request.user.subscription.customer_id,
        return_url=f'{settings.TARGET_URL}/account',
    )

    return HttpResponse(session.url)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({'validation_error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        if not self.object.check_password(serializer.data.get("old_password")):
            return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)

        if not serializer.data.get('new_password') == serializer.data.get('new_password2'):
            return Response({'new_password': ['Passwords must match.']}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(serializer.data.get('new_password'))
        except Exception as ex :
            return Response({'invalid_password': [ex]}, status=status.HTTP_400_BAD_REQUEST)

        self.object.set_password(serializer.data.get('new_password'))
        self.object.save()

        return Response({
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': []
        })


class RequestPasswordResetView(generics.UpdateAPIView):
    serializer_class = serializers.RequestPasswordResetSerializer
    model = account_models.EmailAddress
    permission_classes = [permissions.AllowAny]

    def get_object(self, queryset=None):
        try:
            return account_models.EmailAddress.objects.filter(email=self.request.data.get('email'))[0]
        except IndexError:
            raise http.Http404

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({'validation_error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        self.object.reset_key = get_random_string(length=32)
        self.object.save()

        password_reset_signal.send(sender=self, email=self.object.email, key=self.object.reset_key)

        return Response({
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password reset request sent',
            'data': []
        })

class ResetPasswordView(generics.UpdateAPIView):
    serializer_class = serializers.ResetPasswordSerializer
    model = User
    permission_classes = [permissions.AllowAny,]

    def get_object(self, queryset=None):
        try:
            return User.objects.filter(email_address__reset_key=self.request.data.get('key'))[0]
        except IndexError:
            raise http.Http404

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({'validation_error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        if not serializer.data.get('password') == serializer.data.get('password2'):
            return Response({'password': ['Passwords must match.']}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(serializer.data.get('password'))
        except Exception as ex :
            return Response({'invalid_password': [ex]}, status=status.HTTP_400_BAD_REQUEST)

        self.object.set_password(serializer.data.get('password'))
        self.object.save()
        self.object.email_address.reset_key = None
        self.object.email_address.save()

        return Response({
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': []
        })


class VerifyEmailView(generics.UpdateAPIView):
    queryset = account_models.EmailAddress.objects.all()
    serializer_class = serializers.VerifyEmailSerializer
    model = account_models.EmailAddress
    permission_classes = [permissions.AllowAny,]
    lookup_field = 'verify_key'

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.verified = True
        self.object.verify_key = None
        self.object.save()

        return Response({
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Email address verified successfully',
            'data': []
        })

