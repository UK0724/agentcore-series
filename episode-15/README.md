# Episode 15: Web Search (Fresh Facts with Sources)

Companion code for **Episode 15** of the **AWS AgentCore Complete Guide** series.

Models stop at their training date. AgentCore Web Search is a search tool on the gateway that returns **links, dates and snippets**, with domain filters set by admins, so answers can cite sources. This demo searches a pretend web (`search/index.json`) shaped like the real connector.

Everything runs locally for free. Nothing is deployed to AWS and no AWS resources are created.

---

## Quick Start (Free Local Demo)

### 1. Prerequisites

- Python 3.10+
- A Google Gemini API key (free tier available at [Google AI Studio](https://aistudio.google.com/))

### 2. Setup Environment

```bash
cd episode-15
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

1. Agent page:
   ```bash
   python agent/agent.py
   ```

Open your browser to:
[http://localhost:3023](http://localhost:3023)

---

## File Overview

- [`agent/agent.py`](./agent/agent.py) - An agent with web search. On AWS the tool comes from a Gateway connector; here it is our pretend search. Port 3023.
- [`agent/index.html`](./agent/index.html) - The demo page.
- [`search/index.json`](./search/index.json) - Demo data.
- [`search/web_search.py`](./search/web_search.py) - A pretend web search, shaped like the AgentCore Web Search connector: same limits, a domain filter, and results with a title, URL, snippet and date. The "web" is a tiny local file.
