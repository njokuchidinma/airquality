CO_BREAKPOINTS = [
    {"upper": 4.4, "lower": 0.0, "aqi_high": 50, "aqi_low": 0},       # Good
    {"upper": 9.4, "lower": 4.5, "aqi_high": 100, "aqi_low": 51},     # Moderate
    {"upper": 12.4, "lower": 9.5, "aqi_high": 150, "aqi_low": 101},   # Unhealthy for Sensitive Groups
    {"upper": 15.4, "lower": 12.5, "aqi_high": 200, "aqi_low": 151},  # Unhealthy for Sensitive Groups
    {"upper": 30.4, "lower": 15.5, "aqi_high": 300, "aqi_low": 201},  # Unhealthy
    {"upper": 40.4, "lower": 30.5, "aqi_high": 400, "aqi_low": 301},  # Very Unhealthy
    {"upper": 50.4, "lower": 40.5, "aqi_high": 500, "aqi_low": 401}   # Hazardous
]

CO2_BREAKPOINTS = [
    {"upper": 1000, "lower": 0, "aqi_high": 50, "aqi_low": 0},       # Good
    {"upper": 1500, "lower": 1001, "aqi_high": 100, "aqi_low": 51},  # Moderate
    {"upper": 2000, "lower": 1501, "aqi_high": 150, "aqi_low": 101}, # Unhealthy for Sensitive Groups
    {"upper": 5000, "lower": 2001, "aqi_high": 200, "aqi_low": 151}, # Unhealthy for Sensitive Groups
    {"upper": 10000, "lower": 5001, "aqi_high": 300, "aqi_low": 201},# Unhealthy
    {"upper": 20000, "lower": 10001, "aqi_high": 400, "aqi_low": 301},# Very Unhealthy
    {"upper": 50000, "lower": 20001, "aqi_high": 500, "aqi_low": 401}# Hazardous
]

LPG_BREAKPOINTS = [
    {"upper": 50, "lower": 0, "aqi_high": 50, "aqi_low": 0},         # Good
    {"upper": 100, "lower": 51, "aqi_high": 100, "aqi_low": 51},     # Moderate
    {"upper": 200, "lower": 101, "aqi_high": 150, "aqi_low": 101},   # Unhealthy for Sensitive Groups
    {"upper": 500, "lower": 201, "aqi_high": 200, "aqi_low": 151},   # Unhealthy for Sensitive Groups
    {"upper": 1000, "lower": 501, "aqi_high": 300, "aqi_low": 201},  # Unhealthy
    {"upper": 2000, "lower": 1001, "aqi_high": 400, "aqi_low": 301}, # Very Unhealthy
    {"upper": 5000, "lower": 2001, "aqi_high": 500, "aqi_low": 401}  # Hazardous
]

SMOKE_BREAKPOINTS = [
    {"upper": 12, "lower": 0, "aqi_high": 50, "aqi_low": 0},          # Good
    {"upper": 35.4, "lower": 12.1, "aqi_high": 100, "aqi_low": 51},   # Moderate
    {"upper": 55.4, "lower": 35.5, "aqi_high": 150, "aqi_low": 101},  # Unhealthy for Sensitive Groups
    {"upper": 150.4, "lower": 55.5, "aqi_high": 200, "aqi_low": 151}, # Unhealthy for Sensitive Groups
    {"upper": 250.4, "lower": 150.5, "aqi_high": 300, "aqi_low": 201},# Unhealthy
    {"upper": 350.4, "lower": 250.5, "aqi_high": 400, "aqi_low": 301},# Very Unhealthy
    {"upper": 500.4, "lower": 350.5, "aqi_high": 500, "aqi_low": 401} # Hazardous
]

def calculate_health_condition(aqihc):
    if aqihc <= 50:
        return "Good"
    elif aqihc <= 100:
        return "Moderate"
    elif aqihc <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqihc <= 200:
        return "Unhealthy for Sensitive Groups"
    elif aqihc <= 300:
        return "Unhealthy"
    elif aqihc <= 400:
        return "Very Unhealthy"                 
    else:
        return "Hazardous"

def calculate_aqi_component(concentration, breakpoints):
    """Takes concentration and AQI breakpoints to compute the AQI for each pollutant."""
    for bp in breakpoints:
        if concentration <= bp["upper"]:
            aqi = ((bp["aqi_high"] - bp["aqi_low"]) / (bp["upper"] - bp["lower"])) * (concentration - bp["lower"]) + bp["aqi_low"]
            return aqi
    return 500  # Max AQI for extreme levels

def calculate_general_aqi(data):
    # Extract sensor data from input
    co_concentration = data["co"]
    co2_concentration = data["co2"]
    lpg_concentration = data["lpg"]
    smoke_concentration = data["smoke"]

    # Calculate AQI for each pollutant
    co_aqi = calculate_aqi_component(co_concentration, CO_BREAKPOINTS)
    co2_aqi = calculate_aqi_component(co2_concentration, CO2_BREAKPOINTS)
    lpg_aqi = calculate_aqi_component(lpg_concentration, LPG_BREAKPOINTS)
    smoke_aqi = calculate_aqi_component(smoke_concentration, SMOKE_BREAKPOINTS)

    # Aggregate AQI by taking the max value (worst case scenario)
    overall_aqi = max(co_aqi, co2_aqi, lpg_aqi, smoke_aqi)
    
    health_condition = calculate_health_condition(overall_aqi)

    return overall_aqi, health_condition

# # Example input data from sensor
# sensor_data = {
#     "co": 6.0,    # ppm
#     "co2": 1200,  # ppm
#     "lpg": 80,    # ppm
#     "smoke": 45,  # arbitrary units
# }

# # Calculate the overall AQI
# aqi_result = calculate_general_aqi(sensor_data)
# print(f"Overall AQI: {aqi_result}")