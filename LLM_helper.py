from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

# Updated to use a currently supported Groq model
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"), 
    model_name="llama-3.3-70b-versatile"  # Updated: llama3-70b-8192 was decommissioned
)

if __name__ == "__main__":
    response = llm.invoke("What are the two main ingredients in samosa")
    print(response.content)

