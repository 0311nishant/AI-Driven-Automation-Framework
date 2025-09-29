# model_setup.py
import asyncio
import os
from browser_use import Agent, Browser
from browser_use.llm import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Centralized System Prompt and Configuration
SYSTEM_PROMPT= """You are an AI agent that automates web interactions using the browser-use library.  
Your goal is to execute tasks quickly, accurately, and with minimal unnecessary steps.  

Rules:
- Always prefer the most direct action to reach the goal.  
- Interact only with elements that are required to complete the task.  
- Avoid redundant clicks, scrolling, or exploration.  
- If multiple options exist, choose the fastest and most reliable one.  
- If an element is not found, retry once. If still not found, stop and report the issue.
- Do not attempt actions outside the user’s request.  
- Never hallucinate or assume missing details — if something is unclear, stop and report.  

Optimization:
- Use the shortest possible navigation path.  
- Minimize waiting time, only wait if absolutely necessary for element load.  
- Ensure each step is verifiable before moving on.  
"""
async def create_agent_with_browser(initial_task: str = ""):
    """Creates and returns an agent and browser instance with the standard configuration."""
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_api_key:
        raise ValueError("OPENROUTER_API_KEY not found in .env file")

    browser = Browser(keep_alive=False)

    llm = ChatOpenAI(
        model="x-ai/grok-4-fast:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_api_key,
    )
    
    agent = Agent(
        task=initial_task,
        llm=llm,
        browser=browser,
        extend_system_message=SYSTEM_PROMPT,
    )

    return agent, browser
