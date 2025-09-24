import asyncio
from unittest import TestCase

from autogit.utils.throttled_tasks_executor import ThrottledTasksExecutor


class ThrottledTasksExecutorTests(TestCase):
    async def generate_greeting(self, name: str) -> str:
        await asyncio.sleep(0.1)
        return f'Hello, {name}!'

    def test_throttled_task_execution(self):
        generated_greetings = []

        def process_result(greeting: str) -> None:
            generated_greetings.append(greeting)

        with ThrottledTasksExecutor(delay_between_tasks=0.05) as executor:
            executor.run(self.generate_greeting('World'), callback=process_result)
            executor.run(self.generate_greeting('Universe'), callback=process_result)

        self.assertListEqual(generated_greetings, ['Hello, World!', 'Hello, Universe!'])

    def test_not_throttled_task_execution(self):
        generated_greetings = []

        def process_result(greeting: str) -> None:
            generated_greetings.append(greeting)

        with ThrottledTasksExecutor(delay_between_tasks=0.05) as executor:
            executor.run_not_throttled(
                self.generate_greeting('World'), callback=process_result
            )

        self.assertListEqual(generated_greetings, ['Hello, World!'])

    def test_wait_for_tasks_to_finish(self):
        generated_greetings = []

        def process_result(greeting: str) -> None:
            generated_greetings.append(greeting)

        executor = ThrottledTasksExecutor(delay_between_tasks=0.05)
        executor.start()
        self.assertEqual(executor.is_running, True)
        executor.run_not_throttled(
            self.generate_greeting('World'), callback=process_result
        )
        executor.wait_for_tasks_to_finish()
        executor.stop()

        self.assertEqual(executor.is_running, False)
        self.assertListEqual(generated_greetings, ['Hello, World!'])
