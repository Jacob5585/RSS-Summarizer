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
    response = model = ollama.chat(
        # model='qwen2.5:3b',
        # model='qwen2.5:1.5b',
        model='qwen2.5:0.5b',
        messages = [
            {
                'role': 'system',
                'content': f'Summarize this:\n\n{data}',
            }
            ]
        )

    return response['message']['content']

if __name__ == "__main__":
    pass
    # with open('articles.json', 'r') as file:
    #     content = file.read()

    # response = summarize(content)

    # print(response['message']['content'])
