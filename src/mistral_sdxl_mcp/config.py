import argparse
import os
from dataclasses import dataclass


@dataclass
class AppConfig:
    openai_url: str
    openai_model: str
    comfyui_url: str
    comfyui_workflow_path: str
    mcp_server_url: str
    minio_hostname: str
    minio_access_key: str
    minio_secret_key: str
    mcp_server_listen_port: int
    mcp_server_listen_address: str


class ConfigLoader:
    @staticmethod
    def load() -> AppConfig:
        def require(value, message):
            if value:
                return value
            raise ValueError(message)

        parser = argparse.ArgumentParser(add_help=False)

        parser.add_argument("--openai-url")
        parser.add_argument("--openai-model")
        parser.add_argument("--comfyui-url")
        parser.add_argument("--mcp-server-url")
        parser.add_argument("--minio-host")
        parser.add_argument("--minio-key")
        parser.add_argument("--minio-secret")
        parser.add_argument("--mcp-server-listen-address")
        parser.add_argument("--mcp-server-listen-port")
        parser.add_argument("--comfyui-workflow-path")

        args, _ = parser.parse_known_args()

        cfg = AppConfig(
            openai_url = (
                args.openai_url
                or os.getenv("OPENAI_URL")
                or "http://localhost:5001/v1/chat/completions"
            ),

            openai_model = (
                args.openai_model
                or os.getenv("OPENAI_MODEL")
                or "Ministral-3-14B-Instruct-2512-UD-Q6_K_XL.gguf"
            ),

            comfyui_url = (
                args.comfyui_url
                or os.getenv("COMFYUI_URL")
                or "http://localhost:8188"
            ),

            comfyui_workflow_path=(
                    args.comfyui_url
                    or os.getenv("COMFYUI_WORKFLOW_PATH")
                    or "../tests/data/txt2img.json"
            ),

            mcp_server_url = (
                args.mcp_server_url
                or os.getenv("MCP_SERVER_URL")
                or "ws://127.0.0.1:8765"
            ),

            minio_hostname = (
                args.minio_host
                or os.getenv("MINIO_HOST")
                or "minio.k8s.home.lehadnk.com"
            ),

            mcp_server_listen_address=(
                    args.minio_host
                    or os.getenv("MCP_SERVER_LISTEN_IP")
                    or "127.0.0.1"
            ),

            mcp_server_listen_port=(
                    args.minio_host
                    or os.getenv("MCP_SERVER_LISTEN_PORT")
                    or 8765
            ),

            minio_access_key=require(
                args.minio_key or os.getenv("MINIO_KEY"),
                "Please provide MINIO_KEY"
            ),

            minio_secret_key = require(
                args.minio_secret or os.getenv("MINIO_SECRET"),
                "Please provide MINIO_SECRET"
            )
        )

        return cfg