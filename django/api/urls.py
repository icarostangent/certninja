from django.urls import include, path
from knox import views as knox_views
from rest_framework import routers
from api import views
from api.views import SignUpAPI, SignInAPI, MainUser

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    # path('auth/login', SignInAPI.as_view()),
    # path('auth/logout',knox_views.LogoutView.as_view(), name="knox-logout"),
    # path('auth/register', SignUpAPI.as_view()),
    # path('auth/user', MainUser.as_view()),
    path('auth/', include('knox.urls')),
    path('', include(router.urls)),
]

