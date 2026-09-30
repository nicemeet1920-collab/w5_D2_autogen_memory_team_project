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

    # =========================
    # MODEL
    # =========================

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

If it is reasonable, reply exactly:

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
    # CHECK STATE FILE
    # =========================

    state_file = "states/team_state.json"

    if not os.path.exists(state_file):
        raise FileNotFoundError(
            f"{state_file} not found. Run test_team_state.py first."
        )

    print("State file found.")

    # =========================
    # LOAD STATE
    # =========================

    with open(state_file, "r", encoding="utf-8") as f:
        state = json.load(f)

    print("State JSON loaded.")

    await team.load_state(state)

    print("Team state loaded successfully!")

    # =========================
    # RUN TEAM AFTER LOAD
    # =========================

    print("\n========== RUNNING TEAM AFTER LOAD ==========\n")

    result = await team.run(
        task="Create another practical AI business idea for small shops."
    )

    print("\n========== RESULT ==========\n")

    for message in result.messages:
        print(f"\n[{message.source}]")
        print(message.content)

    print("\nStop reason:")
    print(result.stop_reason)


if __name__ == "__main__":
    asyncio.run(main())