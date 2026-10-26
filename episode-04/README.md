# Episode 4: Gateway and MCP (Your APIs as Agent Tools)

Companion code for **Episode 4** of the **AWS AgentCore Complete Guide** series.

AgentCore Gateway gives your agent **one front door** for every tool. It reads your OpenAPI specs, turns each operation into an MCP tool named `target___operationId`, and translates MCP calls into REST calls. This demo runs two plain REST APIs, a mini gateway that does the same translation, and an agent that only knows the gateway's `/mcp` address.

Everything runs locally for free. Nothing is deployed to AWS and no AWS resources are created.

---

## Quick Start (Free Local Demo)

### 1. Prerequisites

- Python 3.10+
- A Google Gemini API key (free tier available at [Google AI Studio](https://aistudio.google.com/))

### 2. Setup Environment

```bash
cd episode-04
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure API Key

The agent reads `GOOGLE_API_KEY` from the environment. Set it in each terminal that runs a Python piece (see `.env.example`):

```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

```bash
export GOOGLE_API_KEY="your_api_key_here"
```

### 4. Run the Demo

Start each piece in its own terminal, in this order (from the `episode-04` folder):

1. Sprint API (port 4001):
   ```bash
   python apis/sprint_api.py
   ```
2. Team API (port 4002):
   ```bash
   python apis/team_api.py
   ```
3. Mini gateway (port 4000, /mcp):
   ```bash
   python gateway/gateway.py
   ```
4. Agent page:
   ```bash
   python agent/agent.py
   ```

Open your browser to:
[http://localhost:3012](http://localhost:3012)

---

## File Overview

- [`agent/agent.py`](./agent/agent.py) - The agent knows only ONE address: the gateway's /mcp endpoint.
- [`agent/index.html`](./agent/index.html) - The demo page.
- [`apis/sprint-api.openapi.json`](./apis/sprint-api.openapi.json) - OpenAPI spec the gateway reads.
- [`apis/sprint_api.py`](./apis/sprint_api.py) - A normal REST API, nothing to do with AI: sprint data on port 4001.
- [`apis/team-api.openapi.json`](./apis/team-api.openapi.json) - OpenAPI spec the gateway reads.
- [`apis/team_api.py`](./apis/team_api.py) - A second, separate REST API: who is who, on port 4002.
- [`gateway/gateway.py`](./gateway/gateway.py) - A tiny local gateway, to show what AgentCore Gateway does
- [`gateway/targets.json`](./gateway/targets.json) - Gateway targets: which specs to load and their names.
