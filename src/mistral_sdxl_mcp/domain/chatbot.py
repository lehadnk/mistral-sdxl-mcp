import asyncio
import base64
import json

from mistral_sdxl_mcp.api.comfyui import ComfyUIApi
from mistral_sdxl_mcp.api.minio import MinioStorage
from mistral_sdxl_mcp.api.openai import OpenAIApi
from mistral_sdxl_mcp.domain.context_storage import ContextStorage
from mistral_sdxl_mcp.domain.mcp_client import McpClient
import uuid

class Chatbot:
    def __init__(self, ctx_storage: ContextStorage, comfyui_api: ComfyUIApi, openai_api: OpenAIApi, mcp_clients: list[McpClient], s3: MinioStorage):
        self.ctx_storage = ctx_storage
        self.comfyui_api = comfyui_api
        self.openai_api = openai_api
        self.mcp_clients = mcp_clients
        self.s3 = s3

        self.mcp_tools = [tool for mcp_client in mcp_clients for tool in mcp_client.openai_tools()]

    async def run(self):
        self.ctx_storage.add("system", "use only english when creating args for mcp.generate_image request. mcp.generate_image arguments should be set of tags for sdxl image generation. only apply rules above this to mcp requests only. communicate with user in his language.")

        while True:
            input_text = input("Input: ")
            self.ctx_storage.add("user", input_text)

            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.openai_api.request(self.ctx_storage.get(), self.mcp_tools)
            )
            #response = self.openai_api.request(self.ctx_storage.get(), self.mcp_tools)
            if response.status_code == 200:
                await self.handle_response(response.json())
            else:
                self.output(f"Response from openai was {response.status_code}: {response.text}")

    async def handle_response(self, response):
        print(response)
        first_choice = response["choices"][0]
        if first_choice['finish_reason'] == 'stop':
            # text response
            self.output(first_choice['message']['content'])
            self.ctx_storage.add(first_choice['message']['role'], first_choice['message']['content'])
        elif first_choice['finish_reason'] == 'tool_calls':
            self.ctx_storage.remove_last()
            for call in first_choice['message']['tool_calls']:
                tool_response = await self.call_tool(call)

                img_base64 = tool_response["result"]["image_base64"]
                decoded_bytes = base64.b64decode(img_base64)

                url = self.s3.upload_bytes('sdxl-images', f"{uuid.uuid4().hex}.png", decoded_bytes, content_type='image/png')
                self.output(f"Image URL: {url}")

                ctx_message = [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_base64}"
                        }
                    }
                ]
                self.ctx_storage.add(first_choice['message']['role'], ctx_message)


    def output(self, text):
        print(f"Output: {text}")

    async def call_tool(self, call):
        for client in self.mcp_clients:
            for tn in client.tool_names():
                if tn == call['function']['name']:
                    params = json.loads(call['function']['arguments'])
                    response = await client.request(tn, params)

                    return response

        self.output(f"Error: Didn't manage to find tool: {call['function']['name']}")