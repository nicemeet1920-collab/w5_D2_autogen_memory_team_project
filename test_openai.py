import os
import asyncio

from dotenv import load_dotenv
from openai import AsyncOpenAI


load_dotenv()


async def main():

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")

    client = AsyncOpenAI(
        api_key=api_key,
        timeout=30.0,
    )

    print("Sending request to OpenAI...")

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Say hello in one sentence."
            }
        ],
    )

    print("OpenAI response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())