import os
import stripe
from django import http
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password 
from django.http.response import HttpResponse, JsonResponse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, mixins, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from api import models
from api import serializers
from api.permissions import IsOwner
from accounts import models as account_models
from accounts.signals import password_reset_signal


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
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsOwner]


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
    customer = account_models.Subscription.objects.get(user_id=request.data.get('pk'))
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
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    # print(event)
    session = event['data']['object']
    print(f"[*] {event['type']}")

        # print(session.status)

        # client_reference_id = session.status.get('client_reference_id')
        # stripe_customer_id = session.status.get('customer')
        # stripe_subscription_id = session.status.get('subscription')
        # print('--------------------------------------')
        # print(client_reference_id, stripe_customer_id, stripe_subscription_id)

        # user = User.objects.get(id=client_reference_id)
        # StripeCustomer.objects.create(
        #     user=user,
        #     stripeCustomerId=stripe_customer_id,
        #     stripeSubscriptionId=stripe_subscription_id,
        # )
        # print(user.username + ' just subscribed.')

    return HttpResponse(status=200)


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
        
        self.object.reset_key = get_random_string()
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

