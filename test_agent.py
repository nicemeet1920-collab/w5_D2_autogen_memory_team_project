import os
import asyncio

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient


load_dotenv()


async def main():

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")

    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=api_key,
    )

    print("Creating AutoGen agent...")

    agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        system_message="You are a helpful assistant.",
    )

    print("Running AutoGen agent...")

    result = await agent.run(
        task="Say hello in one short sentence."
    )

    print("\n========== RESULT ==========")

    print(result.messages[-1].content)


if __name__ == "__main__":
    asyncio.run(main())