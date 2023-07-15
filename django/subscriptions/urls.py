from django.urls import include, path
from subscriptions import views


urlpatterns = [
    path('customers/<int:pk>/', views.StripeCustomerViewSet.as_view({'get': 'retrieve'})), 
    path('products/', views.StripeProductViewSet.as_view({'get': 'list'})), 
    path('payment/', views.create_payment_intent), 
    path('webhook/', views.stripe_webhook), 
]
