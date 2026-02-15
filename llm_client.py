
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file

api_key = os.getenv("GROQ_API_KEY")

# initialize LLM
llm = ChatGroq(
    api_key=api_key ,
    model="llama-3.1-8b-instant",
    # model = "None",
    temperature=0
)