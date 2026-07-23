import asyncio
import time

tasks = [
    ("Downloading data", 3),
    ("Processing data", 2),
    ("Sending notification", 1),
    ("Saving results", 4),
]


async def do_task(name, delay):
    print(f"{name} started")
    await asyncio.sleep(delay)
    print(f"{name} finished")
    return f"{name} completed"


async def run_sequential():
    start = time.perf_counter()

    results = []
    for name, delay in tasks:
        result = await do_task(name, delay)
        results.append(result)

    end = time.perf_counter()

    print("\nResults:")
    for result in results:
        print(result)

    print(f"\nSequential execution time: {end - start:.2f} seconds")


async def run_concurrent():
    start = time.perf_counter()

    task_list = [do_task(name, delay) for name, delay in tasks]
    results = await asyncio.gather(*task_list)

    end = time.perf_counter()

    print("\nResults:")
    for result in results:
        print(result)

    print(f"\nConcurrent execution time: {end - start:.2f} seconds")


async def main():
    print("=== Sequential Execution ===")
    await run_sequential()

    print("\n=== Concurrent Execution ===")
    await run_concurrent()


asyncio.run(main())