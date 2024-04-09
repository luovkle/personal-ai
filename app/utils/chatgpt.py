import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_completion(input: str) -> str:
    chat_completion = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", ""),
        max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "")),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "")),
        messages=[
            {"role": "user", "content": input},
        ],
        stream=False,
    )
    return chat_completion.choices[0].message.content
