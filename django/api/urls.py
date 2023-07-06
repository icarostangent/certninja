from django.urls import include, path
from rest_framework import routers
from api import views
from api.views import SignUpAPI, MainUser

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    # path('auth/register', SignUpAPI.as_view()),
    # path('auth/user', MainUser.as_view()),
    path('auth/', include('knox.urls')),
    path('', include(router.urls)),
]

