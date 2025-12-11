import asyncio

from mistral_sdxl_mcp.api.minio import MinioStorage
from mistral_sdxl_mcp.api.openai import OpenAIApi
from mistral_sdxl_mcp.api.comfyui import ComfyUIApi
from mistral_sdxl_mcp.config import ConfigLoader
from mistral_sdxl_mcp.domain.chatbot import Chatbot
from mistral_sdxl_mcp.domain.context_storage import ContextStorage
from mistral_sdxl_mcp.domain.mcp_client import McpClient

cfg = ConfigLoader.load()

openai_api = OpenAIApi(
    url=cfg.openai_url,
    model=cfg.openai_model,
)
comfyui_api = ComfyUIApi(
    url=cfg.comfyui_url,
)

ctx_storage = ContextStorage(max_len=8192)

comfyui_mcp_client = McpClient(url=cfg.mcp_server_url)

minio = MinioStorage(
    hostname=cfg.minio_hostname,
    access_key=cfg.minio_access_key,
    secret_key=cfg.minio_secret_key,
)

async def init():
    await comfyui_mcp_client.connect()
    await comfyui_mcp_client.load_tools()
    print(comfyui_mcp_client.tool_names())

    chatbot = Chatbot(ctx_storage, comfyui_api, openai_api, [comfyui_mcp_client], minio)
    await chatbot.run()

asyncio.run(init())