import asyncio
from unittest import TestCase

from gitmultirepoupdater.utils.throttled_tasks_executor import ThrottledTasksExecutor


class ThrottledTasksExecutorTests(TestCase):

    def test_throttled_tasks_executor_callback(self):
        generated_greetings = []

        async def generate_greeting(name: str) -> str:
            await asyncio.sleep(0.1)
            return f"Hello, {name}!"

        def process_result(greeting: str) -> None:
            generated_greetings.append(greeting)

        with ThrottledTasksExecutor(delay_between_tasks=0.2) as executor:
            executor.run(generate_greeting("World"), callback=process_result)
            executor.run(generate_greeting("Universe"), callback=process_result)

        self.assertListEqual(generated_greetings,
                             ["Hello, World!", "Hello, Universe!"])
