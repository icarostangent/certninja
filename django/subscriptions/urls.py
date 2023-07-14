from django.urls import include, path
from subscriptions import views

urlpatterns = [
    path('products/', views.StripeProductViewSet.as_view({'get': 'list'})), 
    path('payment/', views.create_payment_intent), 
    path('webhook/', views.stripe_webhook), 
]
