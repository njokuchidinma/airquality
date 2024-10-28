from django.urls import path
from .views import ReceiveSensorData,ReturnSensorData,UserProfile, RiskAlerts, HealthTips,Authenticate, ChangePassword, ForgotPassword, Logout
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("my-login-user/",Authenticate.as_view()),
    path("user-profile/",UserProfile.as_view()),
    path("get-sensor-data/",ReturnSensorData.as_view()),
    path("receive-sensor-data/",ReceiveSensorData.as_view()),
    path("health-tips/",HealthTips.as_view()),
    path("risk-alerts/",RiskAlerts.as_view()),
    path("change-password/",ChangePassword.as_view()),
    path("forgot-password/",ForgotPassword.as_view()),
    path("logout/",Logout.as_view()),
    path('authenticate-user/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-authentication/', TokenRefreshView.as_view(), name='token_refresh'),
]