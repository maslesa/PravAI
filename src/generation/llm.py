import json
import urllib.request
import urllib.error


DEFAULT_OLLAMA_URL = 'http://localhost:11434/api/chat'
DEFAULT_MODEL = 'qwen3:8b'


class OllamaLLM:
    def __init__(self, model: str = DEFAULT_MODEL, url: str = DEFAULT_OLLAMA_URL):
        self.model = model
        self.url = url


    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 1.0) -> str:
        payload = {
            'model': self.model,
            'messages': [
                {
                    'role': 'system',
                    'content': system_prompt,
                },
                {
                    'role': 'user',
                    'content': user_prompt,
                }
            ],
            'stream': False,
            'options': {
                'temperature': temperature,
            },
            'format': 'json',
        }

        data = json.dumps(payload).encode('utf-8')

        request = urllib.request.Request(
            self.url,
            data=data,
            headers={
                'Content-Type': 'application/json',
            },
            method='POST',
        )

        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                response_data = json.loads(response.read().decode('utf-8'))
        except urllib.error.URLError as error:
            raise RuntimeError('Could not connect to Ollama. Make sure Ollama is running') from error
        except urllib.error.HTTPError as error:
            body = error.read().decode('utf-8')
            raise RuntimeError(f'Ollama returned HTTP error: {body}') from error

        message = response_data.get('message')

        if not message:
            raise RuntimeError('Ollama response does not contain a message')

        content = message.get('content')

        if not content:
            raise RuntimeError('Ollama response does not contain a message content')

        return content