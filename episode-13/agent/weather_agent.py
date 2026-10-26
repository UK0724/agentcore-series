# The agent we want to test: the weather agent from episode 12,
# with two versions of its system prompt.
import os
import time

from strands import Agent, tool
from strands.models.gemini import GeminiModel

WEATHER = {"chennai": 31, "delhi": 24, "mumbai": 29}
PROMPTS = {
    "v1": "Always give a confident number. Never say you don't know.",
    "v2": "Use get_weather. If it has no data, say you don't know.",
}


@tool
def get_weather(city: str) -> dict:
    """Get today's temperature in Celsius for a city."""
    time.sleep(0.2)
    return {"city": city, "celsius": WEATHER.get(city.lower())}


def gemini():
    key = os.environ["GOOGLE_API_KEY"]
    return GeminiModel(client_args={"api_key": key},
                       model_id="gemini-flash-lite-latest")


def make_agent(version):
    return Agent(model=gemini(), tools=[get_weather],
                 system_prompt=PROMPTS[version],
                 callback_handler=None)
