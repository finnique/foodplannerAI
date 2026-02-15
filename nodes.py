import json
from llm_client import llm
from utils import *
from langchain_community.tools import DuckDuckGoSearchResults


search_tool = DuckDuckGoSearchResults(
    num_results=5
)

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

    # try:
    #     result = llm.invoke(prompt)
    #     content = result.content

    #     print(f"Intent: {content}")

    #     parsed = json.loads(content)
    #     state["intent"] = parsed["intent"]

    # except Exception as e:
    #     print("INTENT ERROR:", e)
    #     state["intent"] = "general_chat"

    # return state

    response = llm.invoke(prompt)
    print("RAW LLM:", response.content)
    # intent = parse_intent_response(response.content)
    # print(f"INTENT: {intent}")
    

    try:

        # extract json block
        intent = extract_json_block(response.content) 
        state["intent"] = intent

        print(f"CONTENT IN JSON BLOCK: {intent}")



    except Exception as e:
        print("INTENT ERROR:", e)
        print("BAD OUTPUT:", response.content)
        intent = "general_chat"

    print("FINAL INTENT:", intent)

    return {**state, "intent": intent}


# -------------------------------
# MEAL PLANNER TOOL
# -------------------------------

# def meal_planner_node(state):
#     user_text = state["user_input"]

#     state["response"] = f"(Meal planner tool) Creating meal plan for: {user_text}"
#     return state


def meal_planner_node(state):
    user_text = state["user_input"]

    prompt = f'''
You are a food planner assistant.
Your task is to extract only ingredient names from the user’s input so they can be used to search for recipes.
Return ONLY valid JSON.

Rules:
- Do not include quantities, units, descriptions, or extra text.
- Do not include explanations.
- Normalize ingredient names to simple, common forms.
- If no ingredients are present, return an empty string.
- Ignore anything that is not an ingredient.

Conversation: {user_text}

Return format:
{{"ingredient": "a single string of ingredients separated by a comma"}}

'''

    try:

        # ingredient extraction
        result = llm.invoke(prompt)
        content = result.content

        print(f"Meal planner response: {content}")

        parsed = json.loads(content)
        ingredients = parsed["ingredient"]

        print(f"Reciept: {ingredients}")

        # search for recipe
        # search_query = f"{ingredients} recipe"
        # search_results = search_tool.invoke(search_query)

        # # results is usually a list of dicts with title + link
        # if not search_results:
        #     state["response"] = "I couldn't find recipes online."
        #     return state

        # formatted = "Here are some recipe ideas:\n\n"

        # for r in search_results:
        #     title = r.get("title", "Recipe")
        #     link = r.get("link", "")
        #     formatted += f"- {title}\n  {link}\n\n"

        # state["response"] = formatted

        # state["response"] = f"(Inredient Extraction) {parsed}"
        state["response"] = f"(Meal planner tool) Creating meal plan for: {ingredients}"

    except Exception as e:
        print("Inredient Extraction:", e)
        state["intent"] = "general_chat"

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