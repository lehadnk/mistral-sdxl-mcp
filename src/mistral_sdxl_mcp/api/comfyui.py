import json
import random

import requests
import time

class ComfyUIApi:
    def __init__(self, url: str):
        self.url = url

    def text_to_image(self, workflow: dict, prompt) -> list[str]:
        print(f"Sending task to comfyui: {prompt}...")
        payload = {
            'prompt': self.apply_prompt_to_workflow(workflow, prompt),
            'client_id': f"client_{int(time.time())}_{random.random()}"
        }

        r = requests.post(f"{self.url}/prompt", json=payload)
        prompt_id = r.json()["prompt_id"]

        MAX_RETRIES = 100
        retries = 0
        while True:
            out = requests.get(f"{self.url}/history/{prompt_id}").json()
            if out.get(prompt_id) and out[prompt_id].get("status") and out[prompt_id]["status"].get("completed"):
                break

            retries += 1
            if retries >= MAX_RETRIES:
                break

            time.sleep(0.25)

        filenames = [output['images'][0]['filename'] for output in out[prompt_id]['outputs'].values()]

        return filenames

    def apply_prompt_to_workflow(self, workflow: dict, prompt: str, negative: str = "text, watermark") -> dict:
        wf = json.loads(json.dumps(workflow))  # deep copy

        for node_id in ["6", "15"]:
            if node_id in wf:
                wf[node_id]["inputs"]["text"] = prompt

        for node_id in ["7", "16"]:
            if node_id in wf:
                wf[node_id]["inputs"]["text"] = negative

        return wf

    def get_image_bytes(self, filename: str):
        img = requests.get(
            f"{self.url}/view",
            params={
                "filename": filename,
                "subfolder": ".",
                "type": "output"
            }
        )

        return img.content