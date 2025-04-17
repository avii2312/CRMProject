from django.urls import path

from . import views
from .views import SignupView, EmailVerifyView, CustomLoginView, CustomLogoutView, HomeView, ProtectedDataView

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify-email/', EmailVerifyView.as_view(), name='email_verify'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('home', HomeView.as_view(), name='home'),
    path('api/protected/', ProtectedDataView.as_view(), name='protected'),
]





# from django.urls import path
# from .views import CustomLoginView, CustomLogoutView, HomeView, ProtectedDataView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
#
# urlpatterns = [
#     # Custom authentication views for HTML pages
#     path('login/', CustomLoginView.as_view(), name='login'),
#     path('logout/', CustomLogoutView.as_view(), name='logout'),
#     path('', HomeView.as_view(), name='home'),
#
#     # DRF API endpoint (protected by JWT authentication)
#     path('api/protected/', ProtectedDataView.as_view(), name='protected'),
#
#     # JWT endpoints provided by SimpleJWT (if you need to obtain/refresh tokens via API)
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]
