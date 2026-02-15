## 🍽️ Food Planner AI

Food Planner AI is an intelligent personal assistant designed to help users plan their meals, track ingredients in their fridge, and provide recipe suggestions in real-time. It uses LangGraph, FastAPI, and retrieval-augmented generation to deliver accurate and interactive meal recommendations.

---

### 📝 Features (to be added)

- **Meal Planning** – Suggest daily meals based on user preferences and dietary restrictions.

- **Fridge Inventory Management** – Keep track of what you have in your fridge and factor it into meal suggestions.

- **Interactive Chat** – Communicate with the AI in a chat interface. The AI asks clarifying questions if unsure of the intent.

- **Recipe Retrieval** – Uses DuckDuckGo search to provide real-world recipe links instead of relying solely on generated recipes.

- **Preference Learning** – Remembers user likes/dislikes for future recommendations.

- **Intent Classification** – Determines whether the user wants to plan meals, update fridge inventory, or just chat.
  
---
### 🛠️ Tech Stack

- **Backend:** FastAPI

- A**gent & Workflow:** LangGraph

- **LLM Integration:**  Groq (llama-3.1-8b-instant)

- **Recipe Search:** DuckDuckGo search tool via langchain-community tools

- **Database / Storage:** Optional in-memory or persistent storage for conversation and fridge inventory

- **Deployment:** Docker + AWS (optional)

----
### ⚡ How It Works

- **User Input** – User sends a message, for example: "Plan dinner with chicken."

- **Intent Classification** – The AI determines the user’s goal (meal planning, fridge update, chat).

- **Conditional Routing** – Based on intent, the agent routes the conversation to the correct node.

- **Action Nodes:**

    - Meal Planner: Calls DuckDuckGo search for recipes.

    - Fridge Manager: Updates inventory and uses it for future planning.

    - Chatbot: General conversation.

- **Memory & Preferences** – Stores conversation history and user preferences to improve future suggestions.

- **Response Generation** – Returns suggestions, recipes, or clarifying questions in chat format.
---

<!-- ### 📂 Project Structure
```text
food-planner-ai/
├── main.py               # FastAPI entry point
├── nodes.py              # LangGraph nodes (meal planner, fridge, chat)
├── client.py             # LLM client wrapper
├── graph.py              # LangGraph workflow setup
├── templates/            # Frontend HTML templates
├── static/               # CSS & JS for chat UI
├── requirements.txt
└── README.md -->