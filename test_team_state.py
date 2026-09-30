import os
import asyncio
import json

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

Create one short AI business idea for small shops.
Include:
- Problem
- Customer
- Solution
- Revenue
"""
    )

    critic_agent = AssistantAgent(
        name="critic_agent",
        model_client=model_client,
        system_message="""
You are a Business Critic Agent.

Review the previous business idea.

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
    # RUN TEAM
    # =========================

    print("\n========== RUNNING TEAM ==========\n")

    result = await team.run(
        task="Create an AI business idea for small shops."
    )

    print("\n========== TEAM RESULT ==========\n")

    for message in result.messages:
        print(f"\n[{message.source}]")
        print(message.content)

    print("\nStop reason:")
    print(result.stop_reason)

    # =========================
    # SAVE STATE
    # =========================

    print("\n========== SAVING STATE ==========\n")

    state = await team.save_state()

    os.makedirs("states", exist_ok=True)

    with open("states/team_state.json", "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    print("Team state saved successfully!")
    print("File: states/team_state.json")


if __name__ == "__main__":
    asyncio.run(main())