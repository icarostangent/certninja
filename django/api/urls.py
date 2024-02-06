from django.urls import path
from api import views


agent_list = views.AgentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
agent_detail = views.AgentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
email_list = views.EmailAddressViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
email_detail = views.EmailAddressViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
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
scan_list = views.ScanViewSet.as_view({
    'get': 'list',
})
subscription_detail = views.SubscriptionViewSet.as_view({
    'get': 'retrieve',
})
user_detail = views.UserViewSet.as_view({
    'get': 'retrieve',
})

urlpatterns = [
    path('auth/password/change/', views.ChangePasswordView.as_view(), name='change_password'), 
    path('auth/password/request/', views.RequestPasswordResetView.as_view(), name='request_password_reset'), 
    path('auth/password/reset/', views.ResetPasswordView.as_view(), name='password_reset'), 
    path('auth/register/', views.RegisterViewSet.as_view(), name='auth_register'),
    path('auth/email/verify/<str:verify_key>/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('emails/', email_list, name='email_list'), 
    path('emails/<int:pk>/', email_detail, name='email_detail'), 
    path('domains/', domain_list, name='domain_list'), 
    path('domains/<int:pk>/', domain_detail, name='domain_detail'), 
    path('domains/<int:pk>/scans/', scan_list, name='scan_list'), 
    path('users/<int:pk>/', user_detail, name='user_detail'),
    path('users/<int:pk>/subscription/', subscription_detail, name='user_subscription_detail'),
    # path('users/<int:pk>/emails/', email_list, name='user_email_list'),
    # path('users/<int:pk>/emails/<int:email_pk>/', email_detail, name='user_email_detail'),
    path('users/<int:pk>/agents/', agent_list, name='user_agent_list'), 
    path('users/<int:pk>/agents/<int:agent_pk>/', agent_detail, name='user_agent_detail'), 
    path('webhook/', views.stripe_webhook, name='webhook'), 
    path('portal/', views.get_customer_portal, name='get_customer_portal'), 
    path('service/agent/', views.ServiceAgentView.as_view(), name='service_agent_detail'), 
    path('service/scan/', views.ServiceScanView.as_view(), name='service_scan_detail'), 
]
