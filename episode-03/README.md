# Episode 3: Runtime (Host Your Own Agent Code)

Companion code for **Episode 3** of the **AWS AgentCore Complete Guide** series.

AgentCore Runtime hosts **your own** agent code: any framework, any model. It only needs a tiny contract: `POST /invocations` and `GET /ping` on port 8080, and every session gets its own microVM. This demo wraps a Strands agent with the `BedrockAgentCoreApp` SDK and calls it locally, exactly the way Runtime would.

Everything runs locally for free. Nothing is deployed to AWS and no AWS resources are created.

---

## Quick Start (Free Local Demo)

### 1. Prerequisites

- Python 3.10+
- Node.js 18+
- A Google Gemini API key (free tier available at [Google AI Studio](https://aistudio.google.com/))

### 2. Setup Environment

```bash
cd episode-03
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

Start each piece in its own terminal, in this order (from the `episode-03` folder):

1. Start the agent (the Runtime contract on port 8080):
   ```bash
   python main.py
   ```
2. Start the caller page (plays the part of AgentCore Runtime):
   ```bash
   node client/server.mjs
   ```

Open your browser to:
[http://localhost:3011](http://localhost:3011)

---

## File Overview

- [`client/index.html`](./client/index.html) - The demo page.
- [`client/server.mjs`](./client/server.mjs) - A small caller, playing the part of AgentCore Runtime: it pings the agent and sends invocations with a session ID header, then shows each exchange as a card.
- [`data/sprint.json`](./data/sprint.json) - Demo data.
- [`main.py`](./main.py) - Our own agent code, wrapped for AgentCore Runtime.
- [`tools.py`](./tools.py) - The tools our agent may call.
