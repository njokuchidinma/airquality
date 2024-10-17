from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from .serializers import CustomUserSerializer,SensorDataSerializer,CustomUser,SensorData, HealthTipSerializer, RiskAlertSerializer
from .models import HealthTip, RiskAlert
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
    
    # def post(self,request):
    #     """ THIS IS THE ENDPOINT THE ESP32 SENDS THE SENSOR DATA TO """


    #     data = request.data


    #     data["smoke"] = data["smoke"] *1000_000 - 200

    #     serializer = self.serializer_class(data=data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"data":"ok"},status=status.HTTP_200_OK)
        

    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        """ THIS IS THE ENDPOINT THE ESP32 SENDS THE SENSOR DATA TO """

        data = request.data

        # Validate and save the sensor data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            # Calculate the overall AQI
            aqi = calculate_general_aqi(data)
            health_condition = calculate_health_condition(aqi)

            # Check the request context to decide which data to send (e.g., home page or statistics page)
            if request.query_params.get('page') == 'home':
                # Send general AQI result to the home page
                return Response({"general_aqi": aqi, "health_condition": health_condition}, status=status.HTTP_200_OK)
    
            
            elif request.query_params.get('page') == 'statistics':
                # Send individual sensor data to the statistics page
                return Response({
                    "co": data["co"],
                    "co2": data["co2"],
                    "lpg": data["lpg"],
                    "smoke": data["smoke"],
                    "humidity": data.get("humidity", None),
                    "temperature": data.get("temperature", None),
                    # "general_aqi": aqi,
                    # "health_condition": health_condition
                    }, status=status.HTTP_200_OK)

            return Response({"data": "ok"}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


class ModuleCalibrator(APIView):

    """ THIS IS THE ENDPOINT USED TO CALIBRATE THE READINGS FROM ESP32 """
    def post(self,request):


        return Response({"data":"ok"},status=status.HTTP_200_OK)
    

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


class HealthTip(APIView):
    queryset = HealthTip.objects.all()
    serializer_class = HealthTipSerializer

    def get_queryset(self):
        # Get current time and calculate the cutoff time for tips
        current_time = timezone.now()
        cutoff_time = current_time - timedelta(minutes=30)
        return self.queryset.filter(updated_at__gte=cutoff_time)
    
class RiskAlert(APIView):
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
                if co2_level >= risk.threshold_bad:
                    alerts.append({
                        'title': f'BAD: {risk.element} Alert',
                        'description': f"{co2_level} ppm levels detected. {risk.danger_message} Solution: {risk.solution_message}"
                    })
                elif co2_level >= risk.threshold_high:
                    alerts.append({
                        'title': f'WARNING: {risk.element} Alert',
                        'description': f"{co2_level} ppm levels detected. {risk.danger_message} Solution: {risk.solution_message}"
                    })

            # Check for CO alerts
            elif risk.element.lower() == "carbon monoxide":
                if co_level >= risk.threshold_bad:
                    alerts.append({
                        'title': f'BAD: {risk.element} Alert',
                        'description': f"{co_level} ppm levels detected. {risk.danger_message} Solution: {risk.solution_message}"
                    })
                elif co_level >= risk.threshold_high:
                    alerts.append({
                        'title': f'WARNING: {risk.element} Alert',
                        'description': f"{co_level} ppm levels detected. {risk.danger_message} Solution: {risk.solution_message}"
                    })

            # Check for LPG alerts
            elif risk.element.lower() == "lpg":
                if lpg_level >= risk.threshold_bad:
                    alerts.append({
                        'title': f'BAD: {risk.element} Alert',
                        'description': f"{lpg_level} ppm levels detected. {risk.danger_message} Solution: {risk.solution_message}"
                    })
                elif lpg_level >= risk.threshold_high:
                    alerts.append({
                        'title': f'WARNING: {risk.element} Alert',
                        'description': f"{lpg_level} ppm levels detected. {risk.danger_message} Solution: {risk.solution_message}"
                    })

            # Check for smoke alerts
            elif risk.element.lower() == "smoke":
                if smoke_level >= risk.threshold_bad:
                    alerts.append({
                        'title': f'BAD: {risk.element} Alert',
                        'description': f"{smoke_level} ppm levels detected. {risk.danger_message} Solution: {risk.solution_message}"
                    })
                elif smoke_level >= risk.threshold_high:
                    alerts.append({
                        'title': f'WARNING: {risk.element} Alert',
                        'description': f"{smoke_level} ppm levels detected. {risk.danger_message} Solution: {risk.solution_message}"
                    })

            # Check for humidity alerts
            elif risk.element.lower() == "humidity":
                if humidity_level >= risk.threshold_bad:
                    alerts.append({
                        'title': f'BAD: {risk.element} Alert',
                        'description': f"{humidity_level}% detected. {risk.danger_message} Solution: {risk.solution_message}"
                    })
                elif humidity_level >= risk.threshold_high:
                    alerts.append({
                        'title': f'WARNING: {risk.element} Alert',
                        'description': f"{humidity_level}% detected. {risk.danger_message} Solution: {risk.solution_message}"
                    })

            # Check for temperature alerts
            elif risk.element.lower() == "temperature":
                if temperature_level >= risk.threshold_bad:
                    alerts.append({
                        'title': f'BAD: {risk.element} Alert',
                        'description': f"{temperature_level}°C detected. {risk.danger_message} Solution: {risk.solution_message}"
                    })
                elif temperature_level >= risk.threshold_high:
                    alerts.append({
                        'title': f'WARNING: {risk.element} Alert',
                        'description': f"{temperature_level}°C detected. {risk.danger_message} Solution: {risk.solution_message}"
                    })

        # Return the list of alerts
        return Response(alerts)