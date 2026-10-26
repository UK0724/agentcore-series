# A tiny local gateway, to show what AgentCore Gateway does:
# read OpenAPI specs, turn each operation into an MCP tool,
# and serve all the tools from ONE /mcp endpoint.
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

import mcp.types as types
import uvicorn
from mcp.server.lowlevel import Server
from starlette.responses import JSONResponse
from starlette.routing import Route

HERE = Path(__file__).parent
TOOLS = {}  # tool name -> how to call the REST API
LOG = []    # every translation, so the page can show it


def load_targets():
    for target in json.loads((HERE / "targets.json").read_text()):
        spec = json.loads((HERE / target["spec"]).read_text())
        base = spec["servers"][0]["url"]
        for path, methods in spec["paths"].items():
            for method, op in methods.items():
                # Tool name = target name + ___ + operation name
                name = f"{target['name']}___{op['operationId']}"
                params = {p["name"]: {"type": "string",
                                      "description": p["description"]}
                          for p in op["parameters"]}
                TOOLS[name] = {
                    "method": method.upper(), "url": base + path,
                    "description": op["description"],
                    "schema": {"type": "object", "properties": params,
                               "required": list(params)},
                }


async def list_tools(ctx, params):  # MCP tools/list
    tools = [types.Tool(name=name, description=t["description"],
                        inputSchema=t["schema"])
             for name, t in TOOLS.items()]
    return types.ListToolsResult(tools=tools)


async def call_tool(ctx, params):  # MCP tools/call
    tool = TOOLS[params.name]
    url = tool["url"].format(**params.arguments)  # MCP -> REST URL
    try:
        body = json.loads(urlopen(url).read())
    except HTTPError as error:
        body = {"error": error.code}
    LOG.append({"tool": params.name, "arguments": params.arguments,
                "rest": f"{tool['method']} {url}", "response": body})
    text = types.TextContent(type="text", text=json.dumps(body))
    return types.CallToolResult(content=[text])


async def log(request):
    return JSONResponse(LOG)


load_targets()
print("Tools:", list(TOOLS))
server = Server("mini-gateway", on_list_tools=list_tools,
                on_call_tool=call_tool)
app = server.streamable_http_app(
    stateless_http=True, custom_starlette_routes=[Route("/log", log)])
uvicorn.run(app, host="localhost", port=4000, log_level="warning")
