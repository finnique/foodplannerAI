from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from graph import chat_graph
from memory import conversation_memory

app = FastAPI()

# =========================
# ERROR MSG.
# =========================

FALLBACK_MESSAGE = (
    "Sorry — I'm having trouble generating a response right now. "
    "Please try again in a moment."
)

# =========================
# Chat UI
# =========================

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Food Planner AI Chat</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        #chat-box {
            background: white;
            padding: 15px;
            height: 70vh;
            overflow-y: auto;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .user {
            text-align: right;
            margin: 8px 0;
        }
        .bot {
            text-align: left;
            margin: 8px 0;
        }
        .bubble {
            display: inline-block;
            padding: 10px 14px;
            border-radius: 16px;
            max-width: 70%;
            line-height: 1.4;
        }
        .user .bubble {
            background: #007bff;
            color: white;
        }
        .bot .bubble {
            background: #e4e6eb;
        }

        /* 👇 textarea styling */
        #user-input {
            width: 80%;
            padding: 10px 12px;
            border-radius: 20px;
            border: 1px solid #ccc;
            font-size: 14px;
            resize: none;
            outline: none;
            height: 38px;
            vertical-align: middle;
        }

        #user-input:focus {
            border-color: #007bff;
        }

        button {
            padding: 10px 16px;
            border-radius: 20px;
            border: none;
            background: #007bff;
            color: white;
            cursor: pointer;
            font-size: 14px;
        }

        button:hover {
            background: #0056b3;
        }
    </style>

</head>
<body>

<h2>🍽️ Food Planner AI Chat</h2>

<div id="chat-box"></div>

<textarea id="user-input" rows="2" placeholder="What do you want to eat?"></textarea>
<button onclick="sendMessage()">Send</button>

<script>
const input = document.getElementById("user-input");

input.addEventListener("keydown", function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    // Show user message
    addMessage(message, "user");
    input.value = "";

    // Send to backend
    const response = await fetch("/query", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ text: message })
    });

    const data = await response.json();
    addMessage(data.answer, "bot");
}

function addMessage(text, sender) {
    const chatBox = document.getElementById("chat-box");
    const div = document.createElement("div");
    div.className = sender;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerText = text;

    div.appendChild(bubble);
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}
</script>

</body>
</html>
"""

# -------------------------------
# REQUEST & RESPONSE MODEL
# -------------------------------

class QueryRequest(BaseModel):
    text: str

class QueryResponse(BaseModel):
    answer: str


# -------------------------------
# ROOT
# -------------------------------

@app.get("/")
async def root():
    return {"message": "Food Planner AI running"}


# -------------------------------
# QUERY ENDPOINT
# -------------------------------
    
@app.post("/query", response_model=QueryResponse)
async def query_llm(payload: QueryRequest):

    try:

        # Add user message to memory
        conversation_memory.append({
            "role": "user",
            "content": payload.text
        })

        initial_state = {
            "messages": conversation_memory,
            "user_input": payload.text,
            "intent": None,
            "response": None
        }

        result = chat_graph.invoke(initial_state)

        # Add assistant response to memory
        conversation_memory.append({
            "role": "assistant",
            "content": result["response"]
        })

        return QueryResponse(answer=result["response"])
    
    except Exception as e:
        print("LLM ERROR:", e)
        answer_text = FALLBACK_MESSAGE

        return QueryResponse(answer=answer_text)