import os
import json
import asyncio

from dotenv import load_dotenv

from autogen_core.memory import ListMemory, MemoryContent

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import (
    TextMentionTermination,
    MaxMessageTermination,
)
from autogen_agentchat.ui import Console

from autogen_ext.models.openai import OpenAIChatCompletionClient


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

STATE_FILE = "states/team_state.json"


# ============================================================
# CREATE MODEL CLIENT
# ============================================================

def create_model_client():

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found in .env"
        )

    return OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=api_key,
    )


# ============================================================
# CREATE MEMORY
# ============================================================

async def create_memory():

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

    return memory


# ============================================================
# CREATE TEAM
# ============================================================

async def create_team():

    model_client = create_model_client()

    memory = await create_memory()

    # --------------------------------------------------------
    # IDEA AGENT
    # --------------------------------------------------------

    idea_agent = AssistantAgent(
        name="idea_agent",
        model_client=model_client,
        memory=[memory],

        system_message="""
You are a Business Idea Agent.

Create practical AI business ideas for small shops.

Consider the user's remembered preferences
when useful.

Include:

- Problem
- Customer
- Solution
- Revenue

Keep the answer concise.
"""
    )

    # --------------------------------------------------------
    # CRITIC AGENT
    # --------------------------------------------------------

    critic_agent = AssistantAgent(
        name="critic_agent",
        model_client=model_client,
        memory=[memory],

        system_message="""
You are a Business Critic Agent.

Review the business idea created by the Idea Agent.

Check:

- Real problem
- Clear customer
- Practical solution
- Revenue possibility

If the idea is reasonable, reply exactly:

APPROVE

Otherwise give one short improvement.
"""
    )

    # --------------------------------------------------------
    # TERMINATION
    # --------------------------------------------------------

    stop_condition = (
        TextMentionTermination("APPROVE")
        | MaxMessageTermination(4)
    )

    # --------------------------------------------------------
    # TEAM
    # --------------------------------------------------------

    team = RoundRobinGroupChat(
        [idea_agent, critic_agent],
        termination_condition=stop_condition,
    )

    return team


# ============================================================
# RUN TEAM
# ============================================================

async def run_team(team):

    print("\n========== RUN TEAM ==========\n")

    result = await team.run(
        task="Create a practical AI business idea for small shops."
    )

    for message in result.messages:

        print(f"\n[{message.source}]")

        print(message.content)

    print("\nStop reason:")
    print(result.stop_reason)


# ============================================================
# WATCH TEAM LIVE
# ============================================================

async def watch_team(team):

    print("\n========== LIVE TEAM EXECUTION ==========\n")

    await Console(
        team.run_stream(
            task="Create a practical AI business idea for small shops."
        )
    )


# ============================================================
# SAVE TEAM STATE
# ============================================================

async def save_team_state(team):

    print("\n========== SAVING STATE ==========\n")

    state = await team.save_state()

    os.makedirs("states", exist_ok=True)

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            state,
            file,
            indent=2
        )

    print("Team state saved successfully!")
    print(f"File: {STATE_FILE}")


# ============================================================
# LOAD TEAM STATE
# ============================================================

async def load_team_state(team):

    print("\n========== LOADING STATE ==========\n")

    if not os.path.exists(STATE_FILE):

        print(
            "State file not found."
        )

        print(
            "Run option 1 first and then save the state."
        )

        return

    with open(
        STATE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        state = json.load(file)

    await team.load_state(state)

    print("Team state loaded successfully!")


# ============================================================
# RESET TEAM
# ============================================================

async def reset_team(team):

    print("\n========== RESETTING TEAM ==========\n")

    await team.reset()

    print("Team reset successfully!")


# ============================================================
# MAIN MENU
# ============================================================

async def main():

    print("\n========================================")
    print("   AUTOGEN AI BUSINESS IDEA TEAM")
    print("========================================")

    team = await create_team()

    while True:

        print("\n")
        print("1. Run Team")
        print("2. Watch Team Live")
        print("3. Save Team State")
        print("4. Load Team State")
        print("5. Reset Team")
        print("6. Exit")

        choice = input("\nEnter your choice: ").strip()

        # ----------------------------------------------------
        # OPTION 1
        # ----------------------------------------------------

        if choice == "1":

            await run_team(team)

        # ----------------------------------------------------
        # OPTION 2
        # ----------------------------------------------------

        elif choice == "2":

            await watch_team(team)

        # ----------------------------------------------------
        # OPTION 3
        # ----------------------------------------------------

        elif choice == "3":

            await save_team_state(team)

        # ----------------------------------------------------
        # OPTION 4
        # ----------------------------------------------------

        elif choice == "4":

            await load_team_state(team)

        # ----------------------------------------------------
        # OPTION 5
        # ----------------------------------------------------

        elif choice == "5":

            await reset_team(team)

        # ----------------------------------------------------
        # OPTION 6
        # ----------------------------------------------------

        elif choice == "6":

            print("\nExiting application...")

            break

        # ----------------------------------------------------
        # INVALID OPTION
        # ----------------------------------------------------

        else:

            print(
                "\nInvalid choice. Please enter 1-6."
            )


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    asyncio.run(main())