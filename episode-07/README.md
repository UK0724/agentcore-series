# Episode 7: Policy with Cedar (Rules Your Agent Cannot Break)

Companion code for **Episode 7** of the **AWS AgentCore Complete Guide** series.

Rules written in a prompt can be talked around. AgentCore Policy checks **every tool call at the gateway** against Cedar rules, with **default deny**. This demo reuses the Episode 4 mini gateway, adds a real Cedar policy engine (`cedarpy`), and shows allowed, denied and default-denied calls.

Everything runs locally for free. Nothing is deployed to AWS and no AWS resources are created.

---

## Quick Start (Free Local Demo)

### 1. Prerequisites

- Python 3.10+
- A Google Gemini API key (free tier available at [Google AI Studio](https://aistudio.google.com/))

### 2. Setup Environment

```bash
cd episode-07
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

Start each piece in its own terminal, in this order (from the `episode-07` folder):

1. Refund API (port 4021):
   ```bash
   python apis/refund_api.py
   ```
2. Mini gateway with policy (port 4000):
   ```bash
   python gateway/gateway.py
   ```
3. Agent page:
   ```bash
   python agent/agent.py
   ```

Open your browser to:
[http://localhost:3015](http://localhost:3015)

---

## File Overview

- [`agent/agent.py`](./agent/agent.py) - The same agent as episode 4. It talks only to the gateway, and the gateway's policy engine decides what may run.
- [`agent/index.html`](./agent/index.html) - The demo page.
- [`apis/refund-api.openapi.json`](./apis/refund-api.openapi.json) - OpenAPI spec the gateway reads.
- [`apis/refund_api.py`](./apis/refund_api.py) - A normal REST API for orders and refunds, port 4021. No AI here.
- [`gateway/gateway.py`](./gateway/gateway.py) - Our mini gateway from episode 4, now with a POLICY ENGINE
- [`gateway/policy.cedar`](./gateway/policy.cedar) - Rules checked by the gateway BEFORE any tool runs.
- [`gateway/targets.json`](./gateway/targets.json) - Gateway targets: which specs to load and their names.
