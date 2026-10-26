// A small caller, playing the part of AgentCore Runtime: it pings the agent
// and sends invocations with a session ID header, then shows each exchange as a card.
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";

const AGENT = "http://localhost:8080";
const SESSION_HEADER = "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id";

async function call(op, prompt, session) {
  if (op === "ping") {
    const res = await fetch(`${AGENT}/ping`);
    return { request: "GET /ping", status: res.status, body: await res.json() };
  }
  const res = await fetch(`${AGENT}/invocations`, {
    method: "POST",
    headers: { "Content-Type": "application/json", [SESSION_HEADER]: session },
    body: JSON.stringify({ prompt }),
  });
  return {
    request: "POST /invocations",
    sent: { headers: { [SESSION_HEADER]: session }, body: { prompt } },
    status: res.status,
    body: await res.json(),
  };
}

createServer(async (req, res) => {
  const url = new URL(req.url, "http://localhost");
  if (url.pathname === "/call") {
    const p = url.searchParams;
    const result = await call(p.get("op"), p.get("prompt"), p.get("session"));
    res.writeHead(200, { "Content-Type": "application/json" });
    return res.end(JSON.stringify(result));
  }
  const page = await readFile(new URL("./index.html", import.meta.url));
  res.writeHead(200, { "Content-Type": "text/html" });
  res.end(page);
}).listen(3011, () => console.log("Caller page on http://localhost:3011"));
