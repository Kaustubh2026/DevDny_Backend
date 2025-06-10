from typing import Dict, Any

def get_event_type_weights(event_type: str) -> Dict[str, float]:
    """
    Returns scoring weights based on event type.
    """
    weights = {
        "cricket": {
            "temperature": 0.3,
            "precipitation": 0.3,
            "wind": 0.2,
            "condition": 0.2
        },
        "wedding": {
            "temperature": 0.25,
            "precipitation": 0.35,
            "wind": 0.15,
            "condition": 0.25
        },
        "hiking": {
            "temperature": 0.3,
            "precipitation": 0.25,
            "wind": 0.25,
            "condition": 0.2
        }
    }
    return weights.get(event_type.lower(), weights["cricket"])

def get_temperature_score(temp: float, event_type: str) -> float:
    """
    Calculate temperature score based on event type.
    """
    if event_type.lower() == "cricket":
        if 20 <= temp <= 28:
            return 1.0
        elif 15 <= temp < 20 or 28 < temp <= 32:
            return 0.7
        elif 10 <= temp < 15 or 32 < temp <= 35:
            return 0.4
        else:
            return 0.0
    elif event_type.lower() == "wedding":
        if 18 <= temp <= 26:
            return 1.0
        elif 15 <= temp < 18 or 26 < temp <= 30:
            return 0.7
        elif 12 <= temp < 15 or 30 < temp <= 33:
            return 0.4
        else:
            return 0.0
    else:  # hiking
        if 15 <= temp <= 25:
            return 1.0
        elif 10 <= temp < 15 or 25 < temp <= 28:
            return 0.7
        elif 5 <= temp < 10 or 28 < temp <= 30:
            return 0.4
        else:
            return 0.0

def get_precipitation_score(precip: float, event_type: str) -> float:
    """
    Calculate precipitation score based on event type.
    """
    if event_type.lower() == "cricket":
        if precip < 0.1:
            return 1.0
        elif precip < 0.2:
            return 0.7
        elif precip < 0.3:
            return 0.4
        else:
            return 0.0
    elif event_type.lower() == "wedding":
        if precip < 0.05:
            return 1.0
        elif precip < 0.15:
            return 0.7
        elif precip < 0.25:
            return 0.4
        else:
            return 0.0
    else:  # hiking
        if precip < 0.15:
            return 1.0
        elif precip < 0.25:
            return 0.7
        elif precip < 0.35:
            return 0.4
        else:
            return 0.0

def get_wind_score(wind: float, event_type: str) -> float:
    """
    Calculate wind score based on event type.
    """
    if event_type.lower() == "cricket":
        if wind < 5.5:  # < 20 km/h
            return 1.0
        elif wind < 8.3:  # < 30 km/h
            return 0.7
        elif wind < 11.1:  # < 40 km/h
            return 0.4
        else:
            return 0.0
    elif event_type.lower() == "wedding":
        if wind < 4.2:  # < 15 km/h
            return 1.0
        elif wind < 6.9:  # < 25 km/h
            return 0.7
        elif wind < 9.7:  # < 35 km/h
            return 0.4
        else:
            return 0.0
    else:  # hiking
        if wind < 6.9:  # < 25 km/h
            return 1.0
        elif wind < 9.7:  # < 35 km/h
            return 0.7
        elif wind < 13.9:  # < 50 km/h
            return 0.4
        else:
            return 0.0

def get_condition_score(condition: str, event_type: str) -> float:
    """
    Calculate weather condition score based on event type.
    """
    condition = condition.lower()
    if event_type.lower() == "cricket":
        if condition in ["clear", "partly cloudy"]:
            return 1.0
        elif condition in ["clouds", "scattered clouds"]:
            return 0.7
        elif condition in ["broken clouds", "overcast clouds"]:
            return 0.4
        else:
            return 0.0
    elif event_type.lower() == "wedding":
        if condition in ["clear"]:
            return 1.0
        elif condition in ["partly cloudy"]:
            return 0.8
        elif condition in ["scattered clouds"]:
            return 0.6
        elif condition in ["broken clouds", "overcast clouds"]:
            return 0.4
        else:
            return 0.0
    else:  # hiking
        if condition in ["clear", "partly cloudy"]:
            return 1.0
        elif condition in ["scattered clouds"]:
            return 0.8
        elif condition in ["broken clouds"]:
            return 0.6
        elif condition in ["overcast clouds"]:
            return 0.4
        else:
            return 0.0 