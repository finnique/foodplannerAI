from typing import TypedDict, List, Dict, Optional


class ChatState(TypedDict):
    messages: List[Dict]          # full conversation
    user_input: str               # latest user message
    intent: Optional[str]         # classified intent
    response: Optional[str]       # final answer