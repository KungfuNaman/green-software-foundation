import requests
from typing import Optional, Dict, Any, Callable

class Ollama:
    def __init__(self, 
                 model: str = "orca-mini",
                 url: str = "http://localhost:11434/api/generate",
                 generation_kwargs: Optional[Dict[str, Any]] = None,
                 system_prompt: Optional[str] = None,
                 template: Optional[str] = None,
                 raw: bool = False,
                 timeout: int = 120,
                 streaming_callback: Optional[Callable[[dict], None]] = None):
        self.model = model
        self.url = url
        self.generation_kwargs = generation_kwargs or {}
        self.system_prompt = system_prompt
        self.template = template
        self.raw = raw
        self.timeout = timeout
        self.streaming_callback = streaming_callback

    def generate(self, prompt: str) -> Any:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "generation_kwargs": self.generation_kwargs,
            "system_prompt": self.system_prompt,
            "template": self.template,
            "raw": self.raw
        }

        response = requests.post(self.url, json=payload, timeout=self.timeout)

        if response.status_code == 200:
            data = response.json()
            if self.streaming_callback:
                for chunk in data.get("chunks", []):
                    self.streaming_callback(chunk)
            return data
        else:
            response.raise_for_status()

# Example usage
if __name__ == "__main__":
    ollama = Ollama()
    prompt = "Tell me a story about a brave knight."
    result = ollama.generate(prompt)
    print(result)