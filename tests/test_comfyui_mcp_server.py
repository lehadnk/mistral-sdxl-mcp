import pytest
import websockets
import json
import base64

from mistral_sdxl_mcp.config import ConfigLoader

cfg = ConfigLoader.load()

@pytest.mark.asyncio
async def test_comfyui_mcp_server():
    async with websockets.connect(cfg.mcp_server_url, max_size=10 * 1024 * 1024) as ws:
        req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "mcp.generate_image",
            "params": {"prompt": "Please generate an image"}
        }

        await ws.send(json.dumps(req))

        status_msg = await ws.recv()
        status = json.loads(status_msg)
        assert status.get("method") == "mcp.status"

        result_msg = await ws.recv()
        result = json.loads(result_msg)

        assert result["id"] == 1
        assert result["result"]["status"] == "completed"

        b64 = result["result"]["image_base64"]
        data = base64.b64decode(b64)
        assert len(data) > 0