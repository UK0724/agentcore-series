# An agent with tracing turned on. Every step becomes an
# OpenTelemetry span, the same format AgentCore Observability
# uses. Here we keep the spans in memory and draw them locally.
import json
import os
from http.server import BaseHTTPRequestHandler
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
    InMemorySpanExporter)
from strands import Agent
from strands.models.gemini import GeminiModel
from strands.telemetry import StrandsTelemetry

from tools import get_weather

HERE = Path(__file__).parent
telemetry = StrandsTelemetry()  # sets up OpenTelemetry tracing
spans = InMemorySpanExporter()  # AgentCore: CloudWatch instead
telemetry.tracer_provider.add_span_processor(
    SimpleSpanProcessor(spans))


def ask(question, session_id):
    spans.clear()
    key = os.environ["GOOGLE_API_KEY"]
    model = GeminiModel(client_args={"api_key": key},
                        model_id="gemini-flash-lite-latest")
    agent = Agent(model=model, tools=[get_weather],
                  callback_handler=None,
                  trace_attributes={"session.id": session_id})
    result = agent(question)
    usage = result.metrics.accumulated_usage
    return {"answer": str(result).strip(), "spans": to_rows(),
            "tokens": usage["totalTokens"]}


def to_rows():  # flatten the spans for the page
    rows = []
    for s in spans.get_finished_spans():
        rows.append({
            "name": s.name, "id": f"{s.context.span_id:x}",
            "parent": f"{s.parent.span_id:x}" if s.parent else None,
            "trace": f"{s.context.trace_id:032x}"[:8],
            "start": s.start_time / 1e9, "end": s.end_time / 1e9,
            "session": s.attributes.get("session.id"),
            "tokens": s.attributes.get("gen_ai.usage.total_tokens"),
        })
    return rows


class Page(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path != "/ask":
            page = (HERE / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            return self.wfile.write(page)
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        body = json.dumps(ask(q["q"], q["session"])).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


print("Agent page on http://localhost:3020")
ThreadingHTTPServer(("localhost", 3020), Page).serve_forever()
