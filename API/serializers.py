from rest_framework.serializers import ModelSerializer, EmailField, CharField
from .models import SensorData,CustomUser,RiskAlert,HealthTip
from rest_framework.exceptions import ValidationError



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


class ForgotPasswordSerializer(ModelSerializer):
    email_address = EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email_address']


class ChangePasswordSerializer(ModelSerializer):
    old_password = CharField(required=True, write_only=True)
    new_password = CharField(required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password']

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError("Old password is incorrect.")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


