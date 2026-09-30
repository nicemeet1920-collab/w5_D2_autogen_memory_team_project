import os
import asyncio

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import (
    TextMentionTermination,
    MaxMessageTermination,
)
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

    print("Creating agents...")

    idea_agent = AssistantAgent(
        name="idea_agent",
        model_client=model_client,
        system_message="""
You are a business idea agent.

Create one simple business idea.
Keep your answer under 30 words.
""",
    )

    critic_agent = AssistantAgent(
        name="critic_agent",
        model_client=model_client,
        system_message="""
You are a business critic.

Review the previous idea.

If it is reasonable, reply exactly:
APPROVE

Otherwise give one short improvement.
""",
    )

    print("Creating termination condition...")

    stop_condition = (
        TextMentionTermination("APPROVE")
        | MaxMessageTermination(4)
    )

    print("Creating team...")

    team = RoundRobinGroupChat(
        [idea_agent, critic_agent],
        termination_condition=stop_condition,
    )

    print("Running team...")

    try:

        result = await asyncio.wait_for(
            team.run(
                task="Create a simple AI business idea for small shops."
            ),
            timeout=60,
        )

        print("\n========== TEAM RESULT ==========")

        for message in result.messages:
            print(f"\n[{message.source}]")
            print(message.content)

        print("\nStop reason:")
        print(result.stop_reason)

    except asyncio.TimeoutError:

        print("\nERROR: Team timed out after 60 seconds.")


if __name__ == "__main__":

    asyncio.run(main())