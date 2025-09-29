# synchronized_executor.py
import os
import asyncio
import time
import datetime
from browser_use import Agent, Browser
from browser_use.llm import ChatOpenAI
from model_setup import SYSTEM_PROMPT

# Directory to save screenshots
SCREENSHOTS_DIR = "screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

class SynchronizedAgentExecutor:
    def __init__(self):
        """Initializes the executor with all required components."""
        self.llm = ChatOpenAI(
            model="x-ai/grok-4-fast:free",
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )
        self.browser = Browser(keep_alive=True)
        self.agent = Agent(
            task="Initial task, will be overridden",
            llm=self.llm,
            browser=self.browser,
            extend_system_message=SYSTEM_PROMPT
        )

    async def task(self, task_prompt: str, assertion_prompt: str = None, timeout: int = 30, poll_frequency: int = 5):
        try:
            print(f"\n[ACTION] Executing task: {task_prompt}")
            
            # Create a temporary agent for the action task
            llm = ChatOpenAI(
                model="x-ai/grok-4-fast:free",
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY"),
            )
            action_agent = Agent(task=task_prompt, llm=llm, browser=self.browser, extend_system_message=SYSTEM_PROMPT)
            await action_agent.run()
            await action_agent.close()

            # Conditionally run the assertion if a prompt is provided
            if assertion_prompt:
                print(f"[ASSERTION] Polling for condition: {assertion_prompt}")
                start_time = time.time()
                final_result = ""
                
                while time.time() - start_time < timeout:
                    assertion_agent = Agent(
                        task=f"{assertion_prompt}. Reply with 'Success' if the condition is met, otherwise explain why it failed.",
                        llm=llm,
                        browser=self.browser,
                        extend_system_message=SYSTEM_PROMPT
                    )
                    try:
                        history = await assertion_agent.run()
                        final_result = history.final_result()
                    finally:
                        await assertion_agent.close()

                    if "success" in final_result.lower():
                        print(f"[ASSERTION] Successful after {int(time.time() - start_time)}s.")
                        return
                    
                    print(f"[ASSERTION] Failed, retrying in {poll_frequency}s. AI response: '{final_result}'")
                    await asyncio.sleep(poll_frequency)
                
                raise AssertionError(f"AI assertion timed out after {timeout}s for prompt: '{assertion_prompt}'\nLast AI response: {final_result}")

        except AssertionError as e:
            # Screenshot and re-raise on failure
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = os.path.join(SCREENSHOTS_DIR, f"failure_{timestamp}.png")
            try:
                if self.browser and self.browser.active_page:
                    await self.browser.active_page.screenshot(path=screenshot_path, full_page=True)
                    print(f"Screenshot saved to: {screenshot_path}")
            except Exception as se:
                print(f"Failed to capture screenshot: {se}")
            raise e

    async def stop(self):
        """Cleanup method to close the agent."""
        if self.agent:
            await self.agent.close()
