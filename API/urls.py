from django.urls import path
from .views import ModuleCalibrator,UserProfile,DataHandler, RiskAlert, HealthTip
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    path("user-profile/",UserProfile.as_view()),
    path("get-sensor-data/",DataHandler.as_view()),
    path("send-sensor-data/",DataHandler.as_view()),
    path("calibrate-module/",ModuleCalibrator.as_view()),
    path("health-tips/",HealthTip.as_view()),
    path("risk-alerts/",RiskAlert.as_view()),
    path('authenticate-user/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-authentication/', TokenRefreshView.as_view(), name='token_refresh'),

]