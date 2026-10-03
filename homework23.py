import asyncio
import time


tasks = [
    ("Downloading data", 3),
    ("Processing data", 2),
    ("Sending notification", 1),
    ("Saving results", 4),
]


async def run_task(name, duration):
    print(f"Task {name} started")

    await asyncio.sleep(duration)

    print(f"Task {name} finished")

    return f"{name} completed"


async def run_sequentially():

    start_time = time.perf_counter()

    results = []

    for name, duration in tasks:
        result = await run_task(name, duration)
        results.append(result)

    end_time = time.perf_counter()

    print(results)
    print(f"Sequential execution time: {end_time - start_time:.2f} seconds")


async def run_concurrently():

    start_time = time.perf_counter()

    task_list = [
        run_task(name, duration)
        for name, duration in tasks
    ]

    results = await asyncio.gather(*task_list)

    end_time = time.perf_counter()

    print(results)
    print(f"Concurrent execution time: {end_time - start_time:.2f} seconds")


async def main():
    await run_sequentially()
    await run_concurrently()


asyncio.run(main())