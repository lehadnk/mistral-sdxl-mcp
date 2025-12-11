from collections import deque


class ContextStorage:
    def __init__(self, max_len: int):
        self.ctx = deque()
        self.max_len = max_len

    def add(self, role: str, content: [str, list]):
        if isinstance(content, str):
            # @todo this way to handle is certainly not optimal in terms of context window usage. {"role": "user", "content": ...} would do the thing better
            content = [{"type": "text", "text": content}]

        self.ctx.append({"role": role, "content": content})
        while self.length() > self.max_len:
            self.shorten()

    def shorten(self):
        self.ctx.popleft()

    def get(self):
        return [x for x in self.ctx]

    def length(self):
        avg_tokens_per_symbol = 0.7
        # @todo idk but it's certainly not anything close to img size in bytes
        avg_image_ctx_len = 1000

        ctx_len = 0
        for x in self.ctx:
            for c in x["content"]:
                if c["type"] == "text":
                    ctx_len += len(c["text"]) * avg_tokens_per_symbol
                if c["type"] == "image_url":
                    ctx_len += avg_image_ctx_len

        return ctx_len

    def remove_last(self):
        self.ctx.pop()