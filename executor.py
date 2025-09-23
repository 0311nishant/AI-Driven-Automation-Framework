# synchronized_executor.py
import os
import asyncio
import time
from browser_use import Agent, Browser
from browser_use.llm import ChatOpenAI
from model_setup import system_prompt


class SynchronizedAgentExecutor:
    def __init__(self, browser: Browser):
        if not isinstance(browser, Browser):
            raise TypeError("Executor must be initialized with a browser-use Browser instance.")
        self.browser = browser

    async def _run_actions_and_assert_async(self, task_prompts: str, assertion_prompt: str = None, timeout: int = 30, poll_frequency: int = 5):
        # Existing async logic...
        print(f"\n[ACTION] Executing tasks: {task_prompts}")
        llm = ChatOpenAI(
            model="x-ai/grok-4-fast:free",
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

        action_agent = Agent(task=task_prompts, llm=llm, browser=self.browser, extend_system_message=system_prompt)
        await action_agent.run()
        await action_agent.close()

        if assertion_prompt:
            print(f"[ASSERTION] Polling for condition: {assertion_prompt}")
            start_time = time.time()
            final_result = ""
            while time.time() - start_time < timeout:
                assertion_agent = Agent(
                    task=f"{assertion_prompt}. Reply with 'Success' if the condition is met, otherwise explain why it failed.",
                    llm=llm,
                    browser=self.browser,
                    extend_system_message=system_prompt
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

    def task(self, task_prompts: list[str], assertion_prompt: str = None, timeout: int = 30, poll_frequency: int = 5):
        """Public synchronous API for running tasks and assertions."""
        return self._run_actions_and_assert_async(task_prompts, assertion_prompt, timeout, poll_frequency)

