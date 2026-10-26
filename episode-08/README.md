# Episode 8: Browser Tool (Agents That Click Around)

Companion code for **Episode 8** of the **AWS AgentCore Complete Guide** series.

Lots of the web has no API. AgentCore Browser gives your agent an **isolated browser session**: actions go in (open, type, click, read) and screenshots come out. This demo runs a website with no API, a small browser service built on Playwright, and an agent that drives it.

Everything runs locally for free. Nothing is deployed to AWS and no AWS resources are created.

---

## Quick Start (Free Local Demo)

### 1. Prerequisites

- Python 3.10+
- Node.js 18+
- A Google Gemini API key (free tier available at [Google AI Studio](https://aistudio.google.com/))

### 2. Setup Environment

```bash
cd episode-08
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt

npm install
npx playwright-core install chromium
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

Start each piece in its own terminal, in this order (from the `episode-08` folder):

1. Website with no API (port 4031):
   ```bash
   python site/site.py
   ```
2. Browser service (port 4032):
   ```bash
   node browser/browser_service.js
   ```
3. Agent page:
   ```bash
   python agent/agent.py
   ```

Open your browser to:
[http://localhost:3016](http://localhost:3016)

Screenshots are saved to `browser/shots/` while the demo runs.

---

## File Overview

- [`agent/agent.py`](./agent/agent.py) - An agent with browser tools. The browser runs in a separate, isolated service; the agent only sends it simple actions.
- [`agent/index.html`](./agent/index.html) - The demo page.
- [`browser/browser_service.js`](./browser/browser_service.js) - A tiny browser service, port 4032, like AgentCore Browser
- [`site/site.py`](./site/site.py) - A website with NO API, port 4031: a parcel tracking page.
