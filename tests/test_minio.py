import base64

from mistral_sdxl_mcp.api.minio import MinioStorage
from mistral_sdxl_mcp.config import ConfigLoader

cfg = ConfigLoader.load()

def test_minio():
    with open("data/rd.png", "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    decoded_bytes = base64.b64decode(img_b64)

    minio = MinioStorage(
        hostname=cfg.minio_hostname,
        access_key=cfg.minio_access_key,
        secret_key=cfg.minio_secret_key,
    )
    url = minio.upload_bytes('sdxl-images', 'rd.png', decoded_bytes, content_type='image/png')

    assert url.endswith("/rd.png")