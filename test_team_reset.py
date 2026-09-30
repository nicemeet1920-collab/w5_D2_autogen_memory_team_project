import os
import asyncio

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
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

    # =========================
    # AGENTS
    # =========================

    idea_agent = AssistantAgent(
        name="idea_agent",
        model_client=model_client,
        system_message="""
You are a Business Idea Agent.

Create practical AI business ideas for small shops.
Keep your answer short.
"""
    )

    critic_agent = AssistantAgent(
        name="critic_agent",
        model_client=model_client,
        system_message="""
You are a Business Critic Agent.

Review the business idea.

If the idea is reasonable, reply exactly:

APPROVE

Otherwise give one short improvement.
"""
    )

    # =========================
    # TERMINATION
    # =========================

    stop_condition = (
        TextMentionTermination("APPROVE")
        | MaxMessageTermination(4)
    )

    # =========================
    # TEAM
    # =========================

    team = RoundRobinGroupChat(
        [idea_agent, critic_agent],
        termination_condition=stop_condition,
    )

    # =========================
    # FIRST RUN
    # =========================

    print("\n========== FIRST RUN ==========\n")

    result = await team.run(
        task="Create an AI business idea for small shops."
    )

    for message in result.messages:
        print(f"\n[{message.source}]")
        print(message.content)

    print("\nStop reason:")
    print(result.stop_reason)

    # =========================
    # RESET
    # =========================

    print("\n========== RESETTING TEAM ==========\n")

    await team.reset()

    print("Team reset successfully!")

    # =========================
    # SECOND RUN
    # =========================

    print("\n========== SECOND RUN AFTER RESET ==========\n")

    result = await team.run(
        task="Create a different AI business idea for small shops."
    )

    for message in result.messages:
        print(f"\n[{message.source}]")
        print(message.content)

    print("\nStop reason:")
    print(result.stop_reason)


if __name__ == "__main__":
    asyncio.run(main())