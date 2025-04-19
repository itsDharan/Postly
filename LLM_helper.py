from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

# Updated to use a currently supported Groq model
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"), 
    model_name="llama3-70b-8192"  # Changed to a supported model
)

if __name__ == "__main__":
    response = llm.invoke("What are the two main ingredients in samosa")
    print(response.content)