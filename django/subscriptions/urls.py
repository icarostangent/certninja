from django.urls import include, path
from subscriptions import views

urlpatterns = [
    path('products/', views.get_products), 
    path('payment/', views.create_payment_intent), 
    path('webhook/', views.stripe_webhook), 
]
