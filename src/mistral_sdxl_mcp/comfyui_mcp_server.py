#!/usr/bin/env python3
import asyncio
import base64
import json

from mistral_sdxl_mcp.api.comfyui import ComfyUIApi
from mistral_sdxl_mcp.config import ConfigLoader
from mistral_sdxl_mcp.domain.mcp_server import McpServer

cfg = ConfigLoader.load()
HOST = cfg.mcp_server_listen_address
PORT = cfg.mcp_server_listen_port
COMFYUI_API_URL = cfg.comfyui_url
WORKFLOW_PATH = cfg.comfyui_workflow_path

comfyui_api = ComfyUIApi(url=COMFYUI_API_URL)
with open(WORKFLOW_PATH, "r", encoding="utf8") as f:
    workflow = json.load(f)

class ComfyUIMcpServer(McpServer):
    def get_routes(self):
        return {"mcp.generate_image": self.generate_image}

    def get_tools(self):
        return [{
            "name": "mcp.generate_image",
            "description": "Generate image via ComfyUI",
            "input_schema": {
                "type": "object",
                "properties": {"prompt": {"type": "string"}},
                "required": ["prompt"]
            }
        }]

    async def generate_image(self, req):
        prompt = req["params"]["prompt"]

        await self.send_notify("mcp.status",{"message": f"Generating image for prompt: {prompt}"})
        print(f"Generating image for prompt: {prompt}")

        loop = asyncio.get_running_loop()
        filenames = await loop.run_in_executor(
            None,
            lambda: comfyui_api.text_to_image(workflow, prompt)
        )

        if not filenames:
            await self.send_response(req["id"], error={
                "code": -32602,
                "message": "No image generated"
            })
            return

        image_bytes = await loop.run_in_executor(
            None,
            lambda: comfyui_api.get_image_bytes(filenames[0])
        )

        b64 = base64.b64encode(image_bytes).decode()

        await self.send_response(req["id"], {
            "status": "completed",
            "image_base64": b64
        })
        print("Image was generated successfully")

async def main():
    server = ComfyUIMcpServer(host=HOST, port=PORT)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())