from django.urls import path
from .views import *
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


schema_view = get_schema_view(
    openapi.Info(
        title="Backend Application Programing Interface",
        default_version='v1',
        description="API documentation for the Buchi app",
    ),
    public=False,
    permission_classes=[permissions.AllowAny],
)



urlpatterns = [
    
    path('signup/', SignupView.as_view(), name='signup'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', Login.as_view(),name='login'),
     path('verify/', VerifyEmail.as_view(),name='verify'),
    path('logout/', logoutapi.as_view(),name='logout'),
    path('seller-signup/', SellerRegistrationAPIView.as_view(), name='seller-signup'),
    # path('contact/', views.contact, name='contact'),
    # path('services/', views.services, name='services'),
    # path('portfolio/', views.portfolio, name='portfolio'),
    # path('blog/', views.blog, name='blog'),
]
 