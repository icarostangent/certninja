from django.urls import include, path
from rest_framework import routers
from api import views


urlpatterns = [
    # path('', include(router.urls)),
    path('customers/<int:pk>/', views.StripeCustomerViewSet.as_view({'get': 'retrieve'})), 
    path('products/', views.StripeProductViewSet.as_view({'get': 'list'})), 
    path('payment/', views.create_payment_intent), 
    path('snippets/', views.SnippetViewSet.as_view({'get': 'list'})),
    path('webhook/', views.stripe_webhook), 
]

