# Our mini gateway from episode 4, now with a POLICY ENGINE:
# every tool call is checked against Cedar rules first,
# outside the agent's code, before the real API is called.
import json

import cedarpy
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


POLICIES = (HERE / "policy.cedar").read_text()


def allowed(tool_name, arguments):
    # Ask the Cedar engine: may this user call this tool?
    numbers = {k: int(v) if str(v).isdigit() else v
               for k, v in arguments.items()}
    request = {"principal": 'User::"uday"',
               "action": f'Action::"{tool_name}"',
               "resource": 'Gateway::"mini-gateway"',
               "context": {"input": numbers}}
    result = cedarpy.is_authorized(request, POLICIES, [])
    return result.decision == cedarpy.Decision.Allow


async def call_tool(ctx, params):  # MCP tools/call
    tool = TOOLS[params.name]
    if not allowed(params.name, params.arguments):
        LOG.append({"tool": params.name,
                    "arguments": params.arguments,
                    "policy": "DENY", "rest": "not called"})
        text = types.TextContent(type="text",
                                 text="Denied by policy.")
        return types.CallToolResult(content=[text], isError=True)
    url = tool["url"].format(**params.arguments)  # MCP -> REST URL
    try:
        body = json.loads(urlopen(url).read())
    except HTTPError as error:
        body = {"error": error.code}
    LOG.append({"tool": params.name, "arguments": params.arguments,
                "policy": "ALLOW",
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
