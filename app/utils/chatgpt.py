import os

from openai import OpenAI, AuthenticationError

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_completion(input: str) -> str | None:
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


def get_completion_message(input: str) -> str:
    error_message = (
        "👷 Hey there! We've encountered an error, but we're already working"
        " to fix it. Thanks for your patience"
    )
    try:
        completion = get_completion(input)
    except AuthenticationError:
        completion = error_message
    else:
        completion = completion or error_message
    return completion
