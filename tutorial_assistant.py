import asyncio
from metagpt.logs import logger
from metagpt.roles.tutorial_assistant import TutorialAssistant

async def main():
    topic = "Write a tutorial about AI Agent for non-developer, focus on usage scenario and besst practice, including open ai gpts,autogen,metagpt"
    role = TutorialAssistant(language="Chinese")
    await role.run(topic)


if __name__ == "__main__":
    asyncio.run(main())