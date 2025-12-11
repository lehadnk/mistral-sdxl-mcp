import json
from mistral_sdxl_mcp.api.comfyui import ComfyUIApi
from mistral_sdxl_mcp.config import ConfigLoader


def test_txt_to_img():
    cfg = ConfigLoader.load()
    api = ComfyUIApi(url=cfg.comfyui_url)

    with open("data/txt2img.json", "r", encoding="utf8") as f:
        workflow = json.load(f)

    filenames = api.text_to_image(workflow, "red, cube")
    assert len(filenames) == 1

    for filename in filenames:
        data = api.get_image_bytes(filename)
        assert data