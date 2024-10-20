from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from .serializers import CustomUserSerializer,SensorDataSerializer,CustomUser,SensorData, HealthTipSerializer, RiskAlertSerializer, RiskAlert, HealthTip
from .utils import return_quality_message
from .aqicalc import calculate_general_aqi, calculate_health_condition
from django.utils import timezone
from datetime import timedelta



class DataHandler(APIView):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get(self,request):
        """ THIS IS THE ENDPOINT CALLS TO GET THE SENSOR DATA FROM THE SERVER """
        
        sensorData = self.queryset.filter(productID=request.user.productID).order_by("-timestamp").first()
        serializer = self.serializer_class(sensorData,many=False)

        return Response({"data":serializer.data},status=status.HTTP_200_OK)
    

# class ModuleCalibrator(APIView):
#     serializer_class = SensorDataSerializer

#     """ THIS IS THE ENDPOINT USED TO CALIBRATE THE READINGS FROM ESP32 """
#     def post(self,request):
#         data = request.data

#         serializer = self.serializer_class(data=data)

#         if serializer.is_valid():
#             serializer.save()

#             aqi_percentage, health_condition = calculate_general_aqi(data)

#             # aqi = calculate_general_aqi(data)
#             # health_condition = calculate_health_condition(aqi)

#             if request.query_params.get('page') == 'home':
#                 return Response({"general_aqi": aqi_percentage, "health_condition": health_condition}, status=status.HTTP_200_OK)

#             elif request.query_params.get('page') == 'statistics':
#                 return Response({
#                     "co": data.get("co"),
#                     "co2": data.get("co2"),
#                     "lpg": data.get("lpg"),
#                     "smoke": data.get("smoke"),
#                     "humidity": data.get("humidity", None),
#                     "temperature": data.get("temperature", None),
#                 }, status=status.HTTP_200_OK)
#             return Response({"data":"ok"},status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ModuleCalibrator(APIView):
    serializer_class = SensorDataSerializer
    """ Endpoint to receive data from ESP32 and save it """
    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Data saved successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """ Unified GET method to retrieve data based on query parameters """
    def get(self, request):
        page = request.query_params.get('page')
        latest_data = self.get_latest_sensor_data()
        if page == 'home':
            aqi_percentage, health_condition = calculate_general_aqi(latest_data)
            return Response({
                "general_aqi": aqi_percentage,
                "health_condition": health_condition
            }, status=status.HTTP_200_OK)
        elif page == 'statistics':
            return Response({
                "carbon_monoxide": latest_data.get("carbon_monoxide"),
                "carbon_dioxide": latest_data.get("carbon_dioxide"),
                "lpg_gas": latest_data.get("lpg_gas"),
                "smoke": latest_data.get("smoke"),
                "humidity": latest_data.get("humidity"),
                "temperature": latest_data.get("temperature"),
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid page parameter"}, status=status.HTTP_400_BAD_REQUEST)

    def get_latest_sensor_data(self):
        """Retrieve the latest sensor data from the database"""
        try:
            latest_data = SensorData.objects.latest('id')
            return {
                "carbon_monoxide": latest_data.carbon_monoxide,
                "carbon_dioxide": latest_data.carbon_dioxide,
                "lpg_gas": latest_data.lpg_gas,
                "smoke": latest_data.smoke,
                "humidity": latest_data.humidity,
                "temperature": latest_data.temperature,
            }
        except SensorData.DoesNotExist:
            return {}

class UserProfile(APIView):
    """ THIS ENDPOINT IS USED TO GET/UPDATE USER INFO ON THE SERVER """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        userSerializer = self.serializer_class(request.user).data
        return Response({"data":userSerializer},status=status.HTTP_200_OK)
    

    def put(self,request):

        user = request.user
        serializer = self.serializer_class(user,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"data":"ok"},status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class HealthTips(APIView):
    queryset = HealthTip.objects.all()
    serializer_class = HealthTipSerializer

    def get_queryset(self):
        # Get current time and calculate the cutoff time for tips
        current_time = timezone.now()
        cutoff_time = current_time - timedelta(minutes=45)
        return self.queryset.filter(timestamp__gte=cutoff_time)
    
    def get(self, request):
        queryset = self.get_queryset()

        latest_tip = queryset.order_by('-timestamp').first()
        previous_tips = queryset.exclude(id=latest_tip.id) if latest_tip else queryset.none()
        response_data = {
            'latest_tip': self.serializer_class(latest_tip).data if latest_tip else None,
            'previous_tips': self.serializer_class(previous_tips, many=True).data
        }
        return Response(response_data)
    
class RiskAlerts(APIView):
    queryset = RiskAlert.objects.all()
    serializer_class = RiskAlertSerializer

    def get(self, request):
        sensor_data = request.query_params  # Assuming sensor data is sent as query params
        alerts = []  # List to hold alerts

        # Example of sensor data expected from query parameters
        co2_level = float(sensor_data.get('co2', 0))  # Carbon Dioxide level
        co_level = float(sensor_data.get('co', 0))  # Carbon Monoxide level
        lpg_level = float(sensor_data.get('lpg', 0))  # LPG level
        smoke_level = float(sensor_data.get('smoke', 0))  # Smoke level
        humidity_level = float(sensor_data.get('humidity', 0))  # Humidity level
        temperature_level = float(sensor_data.get('temperature', 0))  # Temperature level

        # Define the risk elements and thresholds
        risk_elements = RiskAlert.objects.all()

                # Check each risk element against the sensor data
        for risk in risk_elements:
            # Check for CO2 alerts
            if risk.element.lower() == "carbon dioxide":
                alerts.append(return_quality_message(
                    co2_level,
                    risk.element,
                    risk.danger_message,
                    risk.solution_message,
                    risk.threshold_bad,
                    risk.threshold_high
                ))

            # Check for CO alerts
            elif risk.element.lower() == "carbon monoxide":
                alerts.append(return_quality_message(
                    co2_level,
                    risk.element,
                    risk.danger_message,
                    risk.solution_message,
                    risk.threshold_bad,
                    risk.threshold_high
                ))

            # Check for LPG alerts
            elif risk.element.lower() == "lpg":
                alerts.append(return_quality_message(
                    lpg_level,
                    risk.element,
                    risk.danger_message,
                    risk.solution_message,
                    risk.threshold_bad,
                    risk.threshold_high
                ))

            # Check for smoke alerts
            elif risk.element.lower() == "smoke":
                alerts.append(return_quality_message(
                    smoke_level,
                    risk.element,
                    risk.danger_message,
                    risk.solution_message,
                    risk.threshold_bad,
                    risk.threshold_high
                ))

            # Check for humidity alerts
            elif risk.element.lower() == "humidity":
                alerts.append(return_quality_message(
                    humidity_level,
                    risk.element,
                    risk.danger_message,
                    risk.solution_message,
                    risk.threshold_bad,
                    risk.threshold_high
                ))

            # Check for temperature alerts
            elif risk.element.lower() == "temperature":
                alerts.append(return_quality_message(
                    temperature_level,
                    risk.element,
                    risk.danger_message,
                    risk.solution_message,
                    risk.threshold_bad,
                    risk.threshold_high
                ))

        # Return the list of alerts
        return Response(alerts)