import os
import asyncio

from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_core.memory import ListMemory, MemoryContent
from autogen_agentchat.ui import Console
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
    # MEMORY
    # =========================

    memory = ListMemory()

    await memory.add(
        MemoryContent(
            content="The user is interested in AI and automation.",
            mime_type="text/plain"
        )
    )

    await memory.add(
        MemoryContent(
            content="The user prefers practical business ideas.",
            mime_type="text/plain"
        )
    )

    print("Memory created.")

    # =========================
    # IDEA AGENT
    # =========================

    idea_agent = AssistantAgent(
        name="idea_agent",
        model_client=model_client,
        memory=[memory],

        system_message="""
You are a Business Idea Agent.

Create one practical AI business idea.

Include:
- Problem
- Customer
- Solution
- Revenue

Keep the answer short.
"""
    )

    # =========================
    # CRITIC AGENT
    # =========================

    critic_agent = AssistantAgent(
        name="critic_agent",
        model_client=model_client,
        memory=[memory],

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
    # LIVE OBSERVATION
    # =========================

    print("\n========== LIVE TEAM EXECUTION ==========\n")

    await Console(
        team.run_stream(
            task="Create a practical AI business idea for small shops."
        )
    )


if __name__ == "__main__":
    asyncio.run(main())