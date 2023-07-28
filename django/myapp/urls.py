"""
URL configuration for myapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
# from django.views.generic.base import TemplateView
# from dj_rest_auth.registration.views import VerifyEmailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), 
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/register/', include('dj_rest_auth.registration.urls')),
    # re_path(r'^api/auth/verify-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(), name='account_confirm_email'),
    path('django-rq/', include('django_rq.urls')),
    path('monitor/', include('django_prometheus.urls')),
    # path('api/auth/verify-email/', VerifyEmailView.as_view(), name='account_email_verification_sent')
]
