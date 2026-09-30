# 🤖 AutoGen Memory Team Project

A beginner-friendly **multi-agent AI business idea system** built using the **AutoGen Framework** and OpenAI.

This project demonstrates important AutoGen concepts including:

* Memory
* Multi-Agent Teams
* RoundRobinGroupChat
* Termination Conditions
* Team Execution
* Live Team Observation
* Team State Save & Load
* Team Reset

---

## 📌 Project Overview

This project creates a simple AI Business Idea Review Team.

The system contains two agents:

### 1. 💡 Idea Agent

The Idea Agent creates a practical AI business idea for small shops.

It considers the user's stored preferences from memory and generates an idea containing:

* Problem
* Customer
* Solution
* Revenue

### 2. 🔍 Critic Agent

The Critic Agent reviews the business idea.

It checks:

* Is there a real problem?
* Is the customer clear?
* Is the solution practical?
* Is there a revenue opportunity?

If the idea is reasonable, the agent responds:

```text
APPROVE
```

---

# 🏗️ Architecture

```text
                    USER
                      │
                      ▼
              ┌───────────────┐
              │    Memory     │
              │  ListMemory   │
              └───────┬───────┘
                      │
                      ▼
            ┌────────────────────┐
            │ RoundRobin Team    │
            └─────────┬──────────┘
                      │
             ┌────────▼────────┐
             │   Idea Agent    │
             └────────┬────────┘
                      │
             ┌────────▼────────┐
             │  Critic Agent   │
             └────────┬────────┘
                      │
                      ▼
              ┌───────────────┐
              │  Termination  │
              │    APPROVE    │
              └───────┬───────┘
                      │
              ┌───────┴────────┐
              │                │
              ▼                ▼
            STOP            Continue
```

---

# 🧠 AutoGen Concepts Covered

## 1. Memory

The project uses:

```python
ListMemory
```

and:

```python
MemoryContent
```

Example stored information:

```text
The user is interested in AI and automation.

The user prefers practical business ideas.
```

Memory is passed to the agents:

```python
memory=[memory]
```

---

## 2. Multi-Agent System

The project uses two agents:

```text
Idea Agent
     ↓
Critic Agent
```

The agents work together to create and review a business idea.

---

## 3. RoundRobinGroupChat

The team is created using:

```python
RoundRobinGroupChat(
    [idea_agent, critic_agent],
    termination_condition=stop_condition,
)
```

The agents take turns during team execution.

---

## 4. Termination Conditions

The project uses two termination conditions:

```python
TextMentionTermination("APPROVE")
```

and:

```python
MaxMessageTermination(4)
```

They are combined using:

```python
stop_condition = (
    TextMentionTermination("APPROVE")
    | MaxMessageTermination(4)
)
```

The team stops when:

* `APPROVE` is mentioned, or
* the maximum message limit is reached.

---

## 5. Team Operation

The project demonstrates:

```python
team.run()
```

for normal team execution.

Example:

```python
result = await team.run(
    task="Create a practical AI business idea for small shops."
)
```

---

## 6. Live Team Observation

The project also uses:

```python
Console(
    team.run_stream(...)
)
```

This allows the user to observe the team execution as it happens.

Example:

```text
[user]
Create a practical AI business idea for small shops.

[idea_agent]
AI business idea...

[critic_agent]
APPROVE
```

---

# 💾 Team State Management

The project demonstrates saving and loading team state.

### Save State

```python
state = await team.save_state()
```

The state is stored in:

```text
states/team_state.json
```

### Load State

```python
await team.load_state(state)
```

This allows the saved team state to be restored.

> Note: `team_state.json` is excluded from Git using `.gitignore`.

---

# 🔄 Team Reset

The project also demonstrates:

```python
await team.reset()
```

This resets the team so it can start a fresh execution.

---

# 🖥️ Application Menu

The final `app.py` provides a simple menu:

```text
1. Run Team
2. Watch Team Live
3. Save Team State
4. Load Team State
5. Reset Team
6. Exit
```

---

# 📁 Project Structure

```text
autogen_memory_team_project/
│
├── .env
├── .gitignore
├── requirements.txt
├── app.py
│
├── test_openai.py
├── test_agent.py
├── test_team.py
├── test_team_memory.py
├── test_team_console.py
├── test_team_state.py
├── test_team_load_state.py
├── test_team_reset.py
│
├── states/
│   └── team_state.json
│
└── myvenv/
```

---

# 🛠️ Technologies Used

* Python
* AutoGen AgentChat
* AutoGen Core
* AutoGen Extensions
* OpenAI
* python-dotenv
* AsyncIO

---

# ⚙️ Requirements

* Python 3.11+
* OpenAI API Key
* Git
* VS Code

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/nicemeet1920-collab/w5_D2_autogen_memory_team_project.git
```

Move into the project:

```bash
cd w5_D2_autogen_memory_team_project
```

---

## 2. Create Virtual Environment

Windows:

```bash
python -m venv myvenv
```

Activate:

```bash
myvenv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Setup

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

⚠️ **Never upload `.env` to GitHub.**

The `.gitignore` file already excludes it.

---

# ▶️ Run the Application

Activate the virtual environment:

```bash
myvenv\Scripts\activate
```

Run:

```bash
python app.py
```

You will see:

```text
========================================
   AUTOGEN AI BUSINESS IDEA TEAM
========================================

1. Run Team
2. Watch Team Live
3. Save Team State
4. Load Team State
5. Reset Team
6. Exit
```

---

# 🧪 Testing Individual Concepts

The project also contains separate test files created while learning each concept.

### Test OpenAI

```bash
python test_openai.py
```

### Test Assistant Agent

```bash
python test_agent.py
```

### Test Team

```bash
python test_team.py
```

### Test Memory + Team

```bash
python test_team_memory.py
```

### Test Live Observation

```bash
python test_team_console.py
```

### Test Save State

```bash
python test_team_state.py
```

### Test Load State

```bash
python test_team_load_state.py
```

### Test Reset

```bash
python test_team_reset.py
```

---

# 🔐 GitHub Security

The following files/directories are excluded from Git:

```text
.env
myvenv/
__pycache__/
*.pyc
states/*.json
```

This prevents sensitive API keys and local environment files from being committed.

---

# 📚 Learning Outcomes

After completing this project, you will understand how to:

* Create AutoGen agents
* Configure an OpenAI model client
* Add memory to agents
* Build multi-agent teams
* Use `RoundRobinGroupChat`
* Create termination conditions
* Run teams using `team.run()`
* Observe teams using `run_stream()`
* Save team state
* Load team state
* Reset a team
* Build a simple menu-driven AutoGen application

---

# 🎯 Project Goal

The main goal of this project is to understand how multiple AutoGen agents can collaborate to solve a practical business problem.

The project provides a simple foundation for building more advanced systems such as:

* AI Customer Support Teams
* AI Business Research Teams
* AI Marketing Teams
* AI Sales Teams
* AI Content Review Teams
* Multi-Agent SaaS Applications

---

# 👨‍💻 Author

**Thirumurugan**

GitHub:

https://github.com/nicemeet1920-collab

---

# 📌 Project Status

```text
Status: Completed ✅

AutoGen Memory        ✅
Multi-Agent Team      ✅
RoundRobin Team       ✅
Termination           ✅
Team Operation        ✅
Live Observation      ✅
Save State            ✅
Load State            ✅
Reset Team            ✅
GitHub Push           ✅
```
