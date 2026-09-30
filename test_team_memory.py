import os
import asyncio

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import (
    TextMentionTermination,
    MaxMessageTermination,
)

from autogen_core.memory import ListMemory, MemoryContent

from autogen_ext.models.openai import OpenAIChatCompletionClient


load_dotenv()


async def main():

    # -----------------------------------------
    # 1. API KEY
    # -----------------------------------------

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")


    # -----------------------------------------
    # 2. MODEL
    # -----------------------------------------

    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=api_key,
    )


    # -----------------------------------------
    # 3. MEMORY
    # -----------------------------------------

    memory = ListMemory()

    await memory.add(
        MemoryContent(
            content="The user's name is Thiru.",
            mime_type="text/plain",
        )
    )

    await memory.add(
        MemoryContent(
            content="The user is interested in AI and automation.",
            mime_type="text/plain",
        )
    )

    await memory.add(
        MemoryContent(
            content="The user prefers practical business ideas.",
            mime_type="text/plain",
        )
    )

    print("Memory created.")


    # -----------------------------------------
    # 4. IDEA AGENT
    # -----------------------------------------

    idea_agent = AssistantAgent(
        name="idea_agent",
        model_client=model_client,
        memory=[memory],

        system_message="""
You are a Business Idea Agent.

Create simple and practical business ideas.

Consider the user's remembered preferences
when they are useful.

Include:
- Problem
- Customer
- Solution
- Revenue

Keep your answer under 100 words.
""",
    )


    # -----------------------------------------
    # 5. CRITIC AGENT
    # -----------------------------------------

    critic_agent = AssistantAgent(
        name="critic_agent",
        model_client=model_client,
        memory=[memory],

        system_message="""
You are a Business Critic Agent.

Review the business idea.

Check:
- Real problem
- Clear customer
- Practical solution
- Revenue possibility

If the idea is reasonable, reply exactly:

APPROVE

Otherwise give one short improvement.
""",
    )


    # -----------------------------------------
    # 6. TERMINATION
    # -----------------------------------------

    stop_condition = (
        TextMentionTermination("APPROVE")
        | MaxMessageTermination(4)
    )


    # -----------------------------------------
    # 7. TEAM
    # -----------------------------------------

    team = RoundRobinGroupChat(
        [idea_agent, critic_agent],
        termination_condition=stop_condition,
    )


    # -----------------------------------------
    # 8. RUN
    # -----------------------------------------

    print("\nRunning team...\n")

    result = await team.run(
        task="Create a business idea for me."
    )


    # -----------------------------------------
    # 9. RESULT
    # -----------------------------------------

    print("\n========== RESULT ==========")

    for message in result.messages:

        print(f"\n[{message.source}]")
        print(message.content)


    print("\nStop reason:")
    print(result.stop_reason)


if __name__ == "__main__":

    asyncio.run(main())