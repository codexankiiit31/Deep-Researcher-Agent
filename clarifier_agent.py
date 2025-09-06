# clarifier_agent.py
import os
from typing import List
from pydantic import BaseModel
from agents import Agent,OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncOpenAI

def get_gemini_model(model_name="gemini-2.5-flash"):
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY")
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    client = AsyncOpenAI(base_url=base_url, api_key=api_key)
    return OpenAIChatCompletionsModel(model=model_name, openai_client=client)

class ClarificationData(BaseModel):
    questions: List[str]
    

CLARIFY_INSTRUCTIONS = """
You are a Research Clarifier. Given a user’s research query, generate exactly 3 clarifying questions 
that will help focus and refine that query. Return only JSON matching the ClarificationData model.
"""

clarifier_agent = Agent(
    name="ClarifierAgent",
    instructions=CLARIFY_INSTRUCTIONS,
    model=get_gemini_model(),
    output_type=ClarificationData,
)
