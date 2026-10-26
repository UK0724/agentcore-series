# Two small tools, so the trace has something to show.
import time

from strands import tool

WEATHER = {"chennai": 31, "delhi": 24, "mumbai": 29}


@tool
def get_weather(city: str) -> dict:
    """Get today's temperature in Celsius for a city."""
    time.sleep(0.4)  # pretend this is a slow API
    return {"city": city, "celsius": WEATHER.get(city.lower())}
