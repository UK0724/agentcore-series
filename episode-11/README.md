# Episode 11: Payments and x402 (Tiny Payments, Hard Limits)

Companion code for **Episode 11** of the **AWS AgentCore Complete Guide** series.

Agents increasingly pay per use. AgentCore Payments works like a **prepaid card with a limit**: the API answers HTTP 402, the agent pays from a payment session, and retries with a proof. Past the spending cap, nothing is paid and no data comes back. This demo uses **pretend cents only**: no wallet, no blockchain, no real money.

Everything runs locally for free. Nothing is deployed to AWS and no AWS resources are created.

---

## Quick Start (Free Local Demo)

### 1. Prerequisites

- Python 3.10+

### 2. Setup Environment

```bash
cd episode-11
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
# source .venv/bin/activate

# No packages needed: standard library only
```

### 3. Run the Demo

Start each piece in its own terminal, in this order (from the `episode-11` folder):

1. Pretend paid API (port 4061):
   ```bash
   python merchant/merchant.py
   ```
2. Agent page:
   ```bash
   python agent/client.py
   ```

Open your browser to:
[http://localhost:3019](http://localhost:3019)

This demo uses only the Python standard library and makes no model calls, so no API key is needed.

---

## File Overview

- [`agent/client.py`](./agent/client.py) - The agent side: call the paid API, and when it answers 402, pay from the session and retry with the proof. Port 3019.
- [`agent/index.html`](./agent/index.html) - The demo page.
- [`agent/wallet.py`](./agent/wallet.py) - A pretend payment session, like an AgentCore PaymentSession
- [`merchant/merchant.py`](./merchant/merchant.py) - A pretend paid API, port 4061. It asks for payment with HTTP 402, like the x402 idea. PRETEND money only: no wallet, no blockchain, nothing real is ever paid.
