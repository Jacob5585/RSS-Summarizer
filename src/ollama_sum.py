import ollama
from dataclasses import dataclass

@dataclass
class Article:
    title: str = ""
    url: str = ""
    image_url: str = ""
    published_date: str = ""
    summary: str = ""

def summarize(data):
    response = ollama.chat(
        model='qwen2.5:0.5b',
        messages = [
            {
                'role': 'system',
                'content': f'Summarize this:\n\n{data}',
            }
            ]
        )

    return response['message']['content']