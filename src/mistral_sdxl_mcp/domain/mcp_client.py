import asyncio
import json

import websockets
from websockets import State


class McpClient:
    def __init__(self, url: str):
        self.url = url
        self.ws = None
        self.tools = []

        self.request_number = 0

    async def connect(self):
        self.ws = await websockets.connect(self.url, max_size=10*1024*1024)

    async def request(self, method, params=None):
        msg = {
            "jsonrpc": "2.0",
            "id": self.request_number,
            "method": method,
            "params": params or {}
        }
        self.request_number += 1


        await self.ws.send(json.dumps(msg))

        while True:
            # @todo honestly I have no idea what happens here
            try:
                raw = await asyncio.wait_for(self.ws.recv(), timeout=30)
            except asyncio.TimeoutError:
                if self.ws.closed:
                    raise RuntimeError(f"MCP connection closed during recv (code={self.ws.close_code})")
                raise RuntimeError("MCP recv timeout — server not responding")

            if self.ws.state is State.CLOSED:
                raise RuntimeError(f"MCP connection lost (code={self.ws.close_code})")

            data = json.loads(raw)

            # статусное сообщение — пропускаем
            if data.get("method") == "mcp.status":
                print("STATUS:", data["params"]["message"])
                continue

            # это ответ на наш запрос
            if data.get("id") == self.request_number - 1:
                return data

    async def load_tools(self):
        resp = await self.request("mcp.list_tools")
        self.tools = resp["result"]["tools"]
        return self.tools

    def openai_tools(self):
        out = []
        for t in self.tools:
            out.append({
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": t.get("description", ""),
                    "parameters": t.get("input_schema", {"type": "object"})
                }
            })

        return out

    def tool_names(self):
        return [t['name'] for t in self.tools]