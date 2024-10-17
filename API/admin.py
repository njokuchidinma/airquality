from django.contrib import admin
from django.http import HttpRequest
from .models import CustomUser,SensorData,HealthTip,RiskAlert
from django.shortcuts import get_object_or_404
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # model = CustomUser
    fieldsets = (
        (None, {"fields": ("productID", "password")}),
        ("Personal Info", {"fields": ("email_address", "full_name", "country", "gender")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email_address", "full_name", "country", "gender", "password1", "password2"),
        }),
    )
    list_display = ("productID","email_address", "full_name", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "is_active",)
    search_fields = ("email_address", "full_name")
    ordering = ("email_address",)
    filter_horizontal =  ()

    readonly_fields = ("productID","email_address", "full_name")



    def has_add_permission(self, request: HttpRequest) -> bool:
        if request.user.is_superuser == True:
            return True
        return False
    
    def has_change_permission(self, request: HttpRequest,obj=None) -> bool:
        if request.user.is_superuser == True:
            return True
        return False
    

    def has_view_permission(self, request: HttpRequest,obj=None) -> bool:
        if request.user.is_superuser == True:
            return True
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        if request.user.is_superuser == True:
            return True
        return False
    
    def has_module_permission(self, request: HttpRequest) -> bool:
        if request.user.is_superuser == True:
            return True
        return False
    

    def current_user(self,request):
        current_user = get_object_or_404(CustomUser,email_address=request)

        return current_user



@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ["productID","smoke","alcohol","lpg_gas","humidity","temperature","carbon_dioxide","carbon_monoxide","timestamp"]


@admin.register(HealthTip)
class HealthTip(admin.ModelAdmin):
    list_display = ["title", "description", "timestamp"]

@admin.register(RiskAlert)
class RiskAlert(admin.ModelAdmin):
    list_display = ["element", "threshold_high", "threshold_bad", "danger_message", "solution_message", "timestamp"]