import asyncio
import json

import websockets


class McpServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def serve(self):
        async with websockets.serve(self.handle_connection, self.host, self.port, max_size=10*1024*1024):
            print(f"MCP server listening on ws://{self.host}:{self.port}")
            await asyncio.Future()

    def get_routes(self) -> dict:
        return {}

    def get_tools(self) -> list:
        return []

    async def send_response(self, id, result=None, error=None):
        msg = {
            "jsonrpc": "2.0",
            "id": id
        }
        if error is not None:
            msg["error"] = error
        else:
            msg["result"] = result
        await self.ws.send(json.dumps(msg))

    async def send_notify(self, method, params):
        msg = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        await self.ws.send(json.dumps(msg))

    async def handle_connection(self, ws):
        # @todo we need connection pool here
        self.ws = ws
        while True:
            try:
                raw = await self.ws.recv()
                request = json.loads(raw)

                routes = self.get_routes()
                routes['ping'] = self.ping
                routes['mcp.list_tools'] = self.list_tools

                method = routes.get(request['method'])
                if method is None:
                    await self.send_response(request.get("id"), error={
                        "code": -32601,
                        "message": "Unknown method"
                    })
                else:
                    await method(request)
            except websockets.ConnectionClosed:
                break

    async def list_tools(self, req):
        await self.send_response(req["id"], {
            "tools": self.get_tools()
        })

    async def ping(self, req):
        await self.send_response(req["id"], "pong")