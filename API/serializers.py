from rest_framework.serializers import ModelSerializer
from .models import SensorData,CustomUser,RiskAlert,HealthTip



class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("full_name","email_address","gender","country","productID")

        # fields = "__all__"

class SensorDataSerializer(ModelSerializer):
    class Meta:
        model = SensorData
        fields = "__all__"

class HealthTipSerializer(ModelSerializer):
    class Meta:
        model = HealthTip
        fields = '__all__'


class RiskAlertSerializer(ModelSerializer):
    class Meta:
        model = RiskAlert
        fields = '__all__'



