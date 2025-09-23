# AiAssertionHelper.py
from browser_use import Agent, Browser
from browser_use.llm import ChatOpenAI
import os
import asyncio
import time

class AiAssertionHelper:
    def __init__(self, browser: Browser):
        """Initializes the helper with a browser-use Browser instance."""
        if not isinstance(browser, Browser):
            raise TypeError("AiAssertionHelper must be initialized with a browser-use Browser instance.")
        self.browser = browser

    async def _create_and_run_agent_with_polling(self, task_prompt: str, success_phrase: str, timeout: int = 30, poll_frequency: int = 5):
        """
        Creates a temporary agent to run a single task and assert its result, with polling.

        Args:
            task_prompt (str): The prompt for the AI to perform the assertion.
            success_phrase (str): The specific phrase the AI is expected to output on success.
            timeout (int): The maximum time in seconds to wait for the condition.
            poll_frequency (int): The time in seconds to wait between each check.
        """
        llm = ChatOpenAI(
            model="x-ai/grok-4-fast:free",
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPENROUTER_API_KEY"),
        )
        
        start_time = time.time()

        while time.time() - start_time < timeout:
            temp_agent = Agent(task=task_prompt, llm=llm, browser=self.browser)
            history = await temp_agent.run()
            final_result = history.final_result()

            if success_phrase.lower() in final_result.lower():
                print(f"AI assertion successful after {int(time.time() - start_time)} seconds: '{task_prompt}'")
                return
            
            print(f"AI assertion failed, retrying in {poll_frequency}s. AI response: '{final_result}'")
            await asyncio.sleep(poll_frequency)
            
        raise AssertionError(f"AI assertion timed out after {timeout}s for prompt: '{task_prompt}'\nLast AI response: {final_result}")

    async def assert_condition(self, condition_description: str, timeout: int = 30, poll_frequency: int = 5):
        """
        Generic assertion for any condition using natural language, with waiting and polling.

        Args:
            condition_description (str): A natural language description of what to verify.
            timeout (int): Maximum time to wait in seconds.
            poll_frequency (int): How often to check in seconds.
        """
        prompt = f"{condition_description}. Reply with 'Success' if the condition is met, otherwise explain why it failed."
        await self._create_and_run_agent_with_polling(prompt, "Success", timeout, poll_frequency)

