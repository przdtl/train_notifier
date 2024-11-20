import asyncio


def run_async(func):
    loop = asyncio.get_event_loop()

    if loop.is_running():
        asyncio.create_task(func())
    else:
        loop.run_until_complete(func())
