import json
from llm_client import llm


# -------------------------------
# INTENT CLASSIFIER NODE
# -------------------------------

def intent_classifier_node(state):
    messages = state["messages"]

    prompt = f"""
You are an intent classifier for a food planning AI.

Return ONLY valid JSON.

Possible intents:
- meal_plan
- update_preference
- update_fridge
- ask_food_question
- general_chat

Conversation:
{messages}

Return format:
{{"intent": "one_of_the_above"}}
"""

    try:
        result = llm.invoke(prompt)
        content = result.content

        parsed = json.loads(content)
        state["intent"] = parsed["intent"]

    except Exception as e:
        print("INTENT ERROR:", e)
        state["intent"] = "general_chat"

    return state


# -------------------------------
# MEAL PLANNER TOOL
# -------------------------------

def meal_planner_node(state):
    user_text = state["user_input"]

    state["response"] = f"(Meal planner tool) Creating meal plan for: {user_text}"
    return state


# -------------------------------
# UPDATE PREFERENCE TOOL
# -------------------------------

def update_preference_node(state):
    state["response"] = "(Preference tool) Preference saved."
    return state


# -------------------------------
# UPDATE FRIDGE TOOL
# -------------------------------

def update_fridge_node(state):
    state["response"] = "(Fridge tool) Fridge updated."
    return state


# -------------------------------
# GENERAL CHAT (LLM fallback)
# -------------------------------

def general_chat_node(state):
    messages = state["messages"]

    try:
        result = llm.invoke(messages)
        state["response"] = result.content
    except Exception as e:
        print("CHAT ERROR:", e)
        state["response"] = "Sorry, something went wrong."

    return state