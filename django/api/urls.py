from django.urls import include, path
from api import views


# customer_detail = views.StripeCustomerViewSet.as_view({
#     'get': 'retrieve',
# })
domain_list = views.DomainViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
domain_detail = views.DomainViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
product_list = views.StripeProductViewSet.as_view({
    'get': 'list',
})
scan_list = views.ScanViewSet.as_view({
    'get': 'list',
})
user_detail = views.UserViewSet.as_view({
    'get': 'retrieve',
})

urlpatterns = [
    # path('', include(router.urls)),
    # path('customers/user/<int:user>/', customer_detail, name='customer-detail'), 
    path('domains/', domain_list, name='domain-list'), 
    path('domains/<int:pk>/', domain_detail, name='domain-detail'), 
    path('domains/<int:pk>/scans/', scan_list, name='scan-list'), 
    path('payment/', views.create_payment_intent, name='create-payment-intent'), 
    path('products/', product_list, name='product-list'), 
    path('register/', views.RegisterView.as_view(), name='auth-register'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('webhook/', views.stripe_webhook, name='webhook'), 
]
