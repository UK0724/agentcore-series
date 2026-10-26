# The tools our agent may call.
# Each one is a normal Python function plus a description.
import json
from pathlib import Path

from strands import tool

DATA = Path(__file__).parent / "data" / "sprint.json"


@tool
def get_sprint_status(sprint: str) -> dict:
    """Velocity, completed points and blocking bugs for one sprint, like sprint-42."""
    data = json.loads(DATA.read_text())
    if sprint not in data:
        return {"error": f"No sprint called {sprint}"}
    return data[sprint]


ALL_TOOLS = {"get_sprint_status": get_sprint_status}
