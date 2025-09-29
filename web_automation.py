# test.py
import asyncio
from executor import SynchronizedAgentExecutor
from sensitiveData.credentials import Credentials


async def main():
    creds = Credentials("automation01sepnishant@yopmail.com", "Test@123") 
    executor = SynchronizedAgentExecutor()


    await executor.task(
        task_prompt="Go to https://app-pune-cp01-qa-nonprod.databahncloud.com",
        assertion_prompt="assert that user is on login page",
    )
    await executor.task(
        task_prompt=f"Login with username {creds.get_username()} and password {creds.get_password()}",
        assertion_prompt="assert that user is logged in and on the dashboard page", timeout=60, poll_frequency=10
    )

    await executor.task(
        task_prompt="Click on Volume Controller menu with navigating url endpoint as 'manage/controller'",
        assertion_prompt="assert that user is navigated to volume controller page",
    )
    await executor.task(
        task_prompt="Click on New Volume controller button")
    
    await executor.task("Name the volume controller as 'task-driven-automation' add random 4 digit integer at the end")

    await executor.task("Select vc scope as cloud")
    await executor.task("Select the first in the source dropdown list")
    await executor.task("Select the first in the destination dropdown list")
    await executor.task("Select the Type as selective filtering")
    await executor.task("Keep the filter criteria as 'AND' and click on '+Rule' button")
    await executor.task("Select the Attribute as 'hostname' Operator as '=' and value as 'webserver01'")
    await executor.task("Click on create volume controller button")
    await executor.task("Refresh the volume controller by clicking on refresh button")
    await executor.task("Search for the created volume controller in the search box at the top left", assertion_prompt="Assert that volume controller is created and is in Deploying state", timeout=60, poll_frequency=5)
    
    if executor:
        await executor.stop()
        await executor.browser.kill()

if __name__ == "__main__":
    asyncio.run(main())
