import pytest

from mistral_sdxl_mcp.config import ConfigLoader
from mistral_sdxl_mcp.domain.mcp_client import McpClient

cfg = ConfigLoader.load()

@pytest.mark.asyncio
async def test_get_tools():
    client = McpClient(url=cfg.mcp_server_url)
    await client.connect()
    await client.load_tools()

    tools = client.openai_tools()
    assert len(tools) > 0

@pytest.mark.asyncio
async def test_call_tool():
    client = McpClient(url=cfg.mcp_server_url)
    await client.connect()
    await client.load_tools()

    resp = await client.request(
        "mcp.generate_image",
        {"prompt": "red cube"}
    )

    assert resp["result"]["status"] == "completed"
    assert isinstance(resp["result"]["image_base64"], str)
    assert len(resp["result"]["image_base64"]) > 100