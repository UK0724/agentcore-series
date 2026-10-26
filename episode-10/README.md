# Episode 10: Agent Registry (Find the Right Agent)

Companion code for **Episode 10** of the **AWS AgentCore Complete Guide** series.

AWS Agent Registry is one catalog for agents, MCP servers and skills, with an approval flow: **draft, pending, approved**. Search only returns approved records. This demo runs a toy registry seeded from `registry/seed.json` and an agent that searches it.

Everything runs locally for free. Nothing is deployed to AWS and no AWS resources are created.

---

## Quick Start (Free Local Demo)

### 1. Prerequisites

- Python 3.10+
- A Google Gemini API key (free tier available at [Google AI Studio](https://aistudio.google.com/))

### 2. Setup Environment

```bash
cd episode-10
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

Start each piece in its own terminal, in this order (from the `episode-10` folder):

1. Registry service and page (port 4051):
   ```bash
   python registry/registry.py
   ```
2. Agent:
   ```bash
   python agent/agent.py
   ```

Open your browser to:
[http://localhost:3018](http://localhost:3018)

---

## File Overview

- [`agent/agent.py`](./agent/agent.py) - An agent that finds help through the registry: it searches the catalog, and only ever sees records that were approved.
- [`registry/page.html`](./registry/page.html) - The demo page.
- [`registry/registry.py`](./registry/registry.py) - A tiny agent registry, port 4051, like AWS Agent Registry
- [`registry/seed.json`](./registry/seed.json) - Demo data.
