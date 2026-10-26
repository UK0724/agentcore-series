# The weather agent again. Its system prompt now comes from a
# config bundle, so we can swap versions without code changes.
import os
import time

from strands import Agent, tool
from strands.models.gemini import GeminiModel

WEATHER = {"chennai": 31, "delhi": 24, "mumbai": 29}


@tool
def get_weather(city: str) -> dict:
    """Get today's temperature in Celsius for a city."""
    time.sleep(0.2)
    return {"city": city, "celsius": WEATHER.get(city.lower())}


def gemini():
    key = os.environ["GOOGLE_API_KEY"]
    return GeminiModel(client_args={"api_key": key},
                       model_id="gemini-flash-lite-latest")


def make_agent(prompt):
    return Agent(model=gemini(), tools=[get_weather],
                 system_prompt=prompt, callback_handler=None)
