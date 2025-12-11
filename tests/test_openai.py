import base64

import pytest

from mistral_sdxl_mcp.api.openai import OpenAIApi
from mistral_sdxl_mcp.config import ConfigLoader
from mistral_sdxl_mcp.domain.mcp_client import McpClient

cfg = ConfigLoader.load()
api = OpenAIApi(
    url=cfg.openai_url,
    model=cfg.openai_model
)

def test_chat_completion():
    messages = [
        {"role": "system", "content": "Отвечай на китайском языке."},
        {"role": "user", "content": "Проверка связи."}
    ]
    response = api.request(messages)
    assert response.status_code == 200

def test_image_completion():
    with open("data/rd.png", "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Что на изображении?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_b64}"
                        }
                    }
                ]
            }
        ]

    response = api.request(payload)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_mcp_tooling():
    mcp_client = McpClient(url=cfg.mcp_server_url)
    await mcp_client.connect()
    await mcp_client.load_tools()

    messages = [{"role": "user", "content": "Call the tool mcp.generate_image with prompt='red cube'."}]
    response = api.request(messages, tools=mcp_client.openai_tools())
    print(response.json())