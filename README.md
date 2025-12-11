# Setup

Software requirements: Python ≥ 3.13, Poetry  
Prerequisites:  
- Access to an OpenAI-compatible MLLM API  
- A deployed ComfyUI backend and an exported workflow file  
- Access to an S3-compatible storage backend (MinIO is recommended, but any S3 provider will work)

1. Clone the repository: `git clone git@github.com:lehadnk/mistral-sdxl-mcp.git`  
2. Open a terminal and run: `poetry install`  
3. Navigate to the `./src` directory.  
4. Start the MCP server:  
   `python -m mistral_sdxl_mcp.comfyui_mcp_server --minio-key k3s --minio-secret k3s`  
5. Start the CLI client:  
   `python -m mistral_sdxl_mcp.cli --minio-key k3s --minio-secret k3s`  

# Configuration

Both the MCP server and the CLI client can be configured using either command-line arguments or environment variables:

| CLI Argument                   | Environment Variable      | Description                                                               |
|-------------------------------|---------------------------|---------------------------------------------------------------------------|
| `--openai-url`                | `OPENAI_URL`              | URL of the OpenAI-compatible API endpoint                                 |
| `--openai-model`              | `OPENAI_MODEL`            | Model name to use for chat completions                                    |
| `--comfyui-url`               | `COMFYUI_URL`             | Base URL of the ComfyUI API                                               |
| `--comfyui-workflow-path`     | `COMFYUI_WORKFLOW_PATH`   | Path to the ComfyUI workflow JSON file                                    |
| `--mcp-server-url`            | `MCP_SERVER_URL`          | WebSocket URL of a remote MCP server                                      |
| `--minio-host`                | `MINIO_HOST`              | Hostname of the MinIO (or other S3-compatible) storage backend            |
| `--minio-key`                 | `MINIO_KEY`               | MinIO access key (**required**)                                           |
| `--minio-secret`             | `MINIO_SECRET`            | MinIO secret key (**required**)                                           |
| `--mcp-server-listen-address` | `MCP_SERVER_LISTEN_IP`    | IP address the MCP server will listen on                                  |
| `--mcp-server-listen-port`    | `MCP_SERVER_LISTEN_PORT`  | Port the MCP server will listen on                                        |
