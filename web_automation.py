# web_automation.py
import asyncio
from model_setup import create_agent_with_browser
from executor import SynchronizedAgentExecutor

async def main():
    browser = None
    try:
        _, browser = await create_agent_with_browser(initial_task="Go to amazon website")
        executor = SynchronizedAgentExecutor(browser)

        await executor.task(
            task_prompts="Go to amazon website",
            assertion_prompt="User is on Amazon homepage"
        )

        await executor.task(
            task_prompts="Locate the search bar and search for asus laptops",
            assertion_prompt="Verify that the search results page is displaying results with asus laptops"
        )

        await executor.task(
            task_prompts="Check the 16 Gb ram filter checkbox",
            assertion_prompt="Verify that the filter for 16 Gb ram checkbox is checked"
        )

        await executor.task(
            task_prompts="Find the laptop with the highest ratings and add it to the cart",
            assertion_prompt=None
        )

        await executor.task(
            task_prompts="Navigate to the cart and increase the quantity of the last item to 2",
            assertion_prompt="Verify that the cart contains 2 units of the selected laptop"
        )
        
        print("\nAll actions and assertions passed successfully.")
        
    finally:
        if browser:
            await browser.kill()

if __name__ == "__main__":
    asyncio.run(main())
