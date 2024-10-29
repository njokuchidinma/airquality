from rest_framework.serializers import ModelSerializer, EmailField, CharField
from .models import SensorData,CustomUser,RiskAlert,HealthTip
from rest_framework.exceptions import ValidationError



class CreateCustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("full_name","email_address","productID","password")

    def create(self, validated_data):
        user = CustomUser(
            full_name=validated_data["full_name"],
            email_address=validated_data["email_address"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
    
    def to_representation(self, instance):
        user  = super().to_representation(instance)

        del user["password"]
        user["productID"] = instance.productID.hex[:8]
        return user


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("full_name","email_address","gender","country","productID")

class SensorDataSerializer(ModelSerializer):
    class Meta:
        model = SensorData
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["productID"]
        return SensorData.objects.create(productID=user,**validated_data)
    


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


