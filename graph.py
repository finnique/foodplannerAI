# app/graph/chat_graph.py

# from typing import TypedDict, List, Optional
# from langgraph.graph import StateGraph, END
# from llm_client import llm


# # -------------------------
# # Define states
# # -------------------------

# class Message(TypedDict):
#     role: str   # "user" or "assistant"
#     content: str

# class ChatState(TypedDict, total=False):
#     messages: List[Message]
#     user_input: str
#     answer: str



# # takes state -> return updated state
# def llm_node(state: ChatState) -> ChatState:
#     # response = llm.invoke(state["user_input"]) 
#     # response = llm.invoke(state["messages"])

#     # # return new state
#     # return {
#     #     "user_input": state["user_input"],
#     #     "answer": response.content
#     # }

#     # response = llm.invoke(state["messages"])

#     # new_messages = state["messages"] + [
#     #     {"role": "assistant", "content": response.content}
#     # ]

#     # return {
#     #     "messages": new_messages,
#     #     "answer": response.content
#     # }

#     # Get last user message
#     last_user_message = next(
#         (msg["content"] for msg in reversed(state["messages"]) if msg["role"] == "user"),
#         ""
#     )

#     response = llm.invoke(state["messages"])  # send full conversation

#     # Append assistant message
#     new_messages = state["messages"] + [{"role": "assistant", "content": response.content}]

#     print(new_messages)

#     return {
#         "messages": new_messages,
#         "answer": response.content
#     }


# def build_chat_graph():
#     builder = StateGraph(ChatState)

#     builder.add_node("llm", llm_node)
#     builder.set_entry_point("llm")
#     builder.add_edge("llm", END)

#     return builder.compile()


# chat_graph = build_chat_graph()
# from llm_client import llm
from langgraph.graph import StateGraph, END
from state import ChatState
from nodes import (
    intent_classifier_node,
    meal_planner_node,
    update_preference_node,
    update_fridge_node,
    general_chat_node,
)
from router import route_intent


builder = StateGraph(ChatState)

# ---- nodes ----
builder.add_node("intent_classifier", intent_classifier_node)
builder.add_node("meal_planner", meal_planner_node)
builder.add_node("update_preference", update_preference_node)
builder.add_node("update_fridge", update_fridge_node)
builder.add_node("general_chat", general_chat_node)

# ---- entry ----
builder.set_entry_point("intent_classifier")

# ---- routing ----
builder.add_conditional_edges(
    "intent_classifier",
    route_intent,
    {
        "meal_planner": "meal_planner",
        "update_preference": "update_preference",
        "update_fridge": "update_fridge",
        "general_chat": "general_chat",
    },
)

# ---- end ----
builder.add_edge("meal_planner", END)
builder.add_edge("update_preference", END)
builder.add_edge("update_fridge", END)
builder.add_edge("general_chat", END)

chat_graph = builder.compile()
