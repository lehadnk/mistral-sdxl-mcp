import requests
import copy

class OpenAIApi:
    def __init__(self, url: str, model: str):
        self.url = url
        self.model = model

    def request(self, messages: list, tools: list = ()):
        payload = {
            "model": "Ministral-3-14B-Instruct-2512-UD-Q6_K_XL.gguf",
            "messages": messages,
            "tools": tools,
            "temperature": 0.2,
        }
        print(self.shorten_payload_for_log(payload))

        resp = requests.post(self.url, json=payload, timeout=360)
        return resp

    def shorten_payload_for_log(self, payload: dict) -> dict:
        data = copy.deepcopy(payload)

        for msg in data.get("messages", []):
            if not isinstance(msg.get("content"), list):
                continue

            for block in msg["content"]:
                if block.get("type") == "image_url":
                    url = block["image_url"]["url"]
                    if url.startswith("data:image"):
                        shortened = url[:40] + "...<snip>..." + url[-40:]
                        block["image_url"]["url"] = shortened

        return data