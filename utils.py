from collections import Counter
import json
import re

def get_majority_intent(intent_list):
    """
    intent_list = [
        {"intent": "meal_plan"},
        {"intent": "meal_plan"},
        {"intent": "update_fridge"}
    ]
    """

    if not intent_list:
        return "general_chat"

    intents = [item["intent"] for item in intent_list if "intent" in item]

    if not intents:
        return "general_chat"

    most_common = Counter(intents).most_common(1)[0][0]
    return most_common


def parse_intent_response(text: str):
    text = text.strip()

    if text.startswith("```"):
        text = text.split("```")[1]

    data = json.loads(text)

    print("Parsing JSON ===")
    print(f"type: {type(data)}")
    print(f"content: {data}")

    # if model returned ONE intent
    if isinstance(data, dict):
        return data.get("intent", "general_chat")

    # if model returned MULTIPLE intents
    if isinstance(data, list):
        return get_majority_intent(data)

    return "general_chat"

def extract_json_block(llm_response):
    match = re.search(r'\{.*\}', llm_response, re.DOTALL)

    if match:
        json_str = match.group()
        data = json.loads(json_str)
        print(data["intent"])
    else:
        print("No JSON found")

    return data["intent"]