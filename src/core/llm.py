"""OpenAI client wrapper."""

from openai import OpenAI


def get_openai_client(api_key: str) -> OpenAI:
    """Create OpenAI client with given API key."""
    return OpenAI(api_key=api_key)


async def chat_completion(
    client: OpenAI,
    messages: list[dict],
    model: str = "gpt-4o-mini",
    **kwargs
) -> str:
    """Simple chat completion wrapper."""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        **kwargs
    )
    return response.choices[0].message.content
