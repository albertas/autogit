import asyncio
import time
import traceback
from collections.abc import Callable, Coroutine
from sys import version_info
from threading import Thread


class ThrottledTasksExecutor:
    """Executor which allows to run coroutines without hitting throttling limits.

    Usage example:
        async def generate_greeting(name: str) -> str:
            from datetime import datetime
            print(f"Started greeting generation for {name} at {datetime.now()}")
            await asyncio.sleep(1)
            print(f"Done greeting generation for {name} at {datetime.now()}")
            return f"Hello, {name}!"

        def process_result(greeting: str) -> None:
            print(f"This result was generated: {greeting}")

        with ThrottledTasksExecutor(delay_between_tasks=2) as executor:
            executor.run(generate_greeting("World"), callback=process_result)
            executor.run(generate_greeting("Universe"), callback=process_result)
    """

    def __init__(
        self, delay_between_tasks: float = 0.2, in_separate_process: bool = False
    ) -> None:
        self.loop = asyncio.new_event_loop()
        self.running_tasks = (
            set()
        )  # TODO: Find the example with task removal from the set.
        # TODO: Would be nice to have awaitable future, instead of infinite loop.
        self.delay_between_tasks = delay_between_tasks
        self.in_separate_process = in_separate_process

        if version_info.major == 3 and version_info.minor >= 10:
            self.can_task_be_executed = asyncio.Condition()
        else:
            self.can_task_be_executed = asyncio.Condition(loop=self.loop)
        self.is_running = False

    def __enter__(self) -> 'ThrottledTasksExecutor':
        self.start()
        return self

    def __exit__(self, *exc_info) -> None:
        self.wait_for_tasks_to_finish()
        self.stop()

    def start(self, in_separate_process: bool | None = None) -> None:
        """Starts a thread (or a process), which executes coroutines provided to the ThrottledTasksExecutor."""
        if in_separate_process is None:
            in_separate_process = self.in_separate_process

        if in_separate_process:
            # TODO: investigate a way to start coroutines in a separate process:
            #   - https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor
            msg = 'Running executor in a separate process is not supported yet'
            raise NotImplementedError(msg)
        thread = Thread(target=self._run_event_loop, daemon=True)
        thread.start()

        self.is_running = True

        # Periodically emit permission to execute one task
        self._allow_task_execution_task = asyncio.run_coroutine_threadsafe(
            self._allow_task_execution(every=self.delay_between_tasks), self.loop
        )

    def stop(self) -> None:
        """Terminates a thread (or a process), which executes coroutines provided to the ThrottledTasksExecutor."""
        self.is_running = False
        self._allow_task_execution_task.cancel()

        time.sleep(
            self.delay_between_tasks
        )  # Wait for _allow_task_execution_task to be destroyed
        self.loop.stop()

    def run(
        self,
        coroutine: Coroutine | Callable,
        *args,
        callback: Callable | None = None,
        **kwargs,
    ) -> None:
        """Executes coroutine in an executor thread, which makes sure not to hit throttling limits."""
        if callback is None:

            def callback(*args, **kwargs):
                return None

        if not isinstance(coroutine, Coroutine):
            coroutine = coroutine(*args, **kwargs)
        if not isinstance(coroutine, Coroutine):
            msg = 'Can only execute coroutines, not coroutine provided'
            raise ValueError(msg)

        task = asyncio.run_coroutine_threadsafe(
            self._throttled_task(coroutine), self.loop
        )
        self.running_tasks.add(task)
        task.add_done_callback(self._mark_task_done(callback))

    def run_not_throttled(
        self,
        coroutine: Coroutine | Callable,
        *args,
        callback: Callable | None = None,
        **kwargs,
    ) -> None:
        """Executes coroutine in an executor event loop ignoring throttled tasks queue."""
        if callback is None:

            def callback(*args, **kwargs):
                return None

        if not isinstance(coroutine, Coroutine):
            coroutine = coroutine(*args, **kwargs)
        if not isinstance(coroutine, Coroutine):
            msg = 'Can only execute coroutines, not coroutine provided'
            raise ValueError(msg)

        task = asyncio.run_coroutine_threadsafe(coroutine, self.loop)
        self.running_tasks.add(task)
        task.add_done_callback(self._mark_task_done(callback))

    def wait_for_tasks_to_finish(self) -> None:
        asyncio.run(self.async_wait_for_tasks_to_finish())

    async def async_wait_for_tasks_to_finish(self) -> None:
        while self.running_tasks:
            await asyncio.sleep(0.1)

    async def _allow_task_execution(self, every: float, count: int = 1) -> None:
        """Periodically emits event, which allows for `count` tasks to be executed.

        Params:
            every: float  - seconds how often a permission is given to `count` tasks to be executed.
            count: int    - how many tasks are allowed to be run at each event.
        """
        try:
            while self.is_running:
                # Does the first task has to wait `every` seconds to be started?
                async with self.can_task_be_executed:
                    if count and count > 0:
                        self.can_task_be_executed.notify(n=count)
                    else:
                        self.can_task_be_executed.notify_all()
                await asyncio.sleep(every)
        except asyncio.CancelledError:
            pass

    def _throttled_task(self, coroutine: Coroutine) -> Coroutine:
        """Decorator for coroutine to wait for permission before executing the coroutine."""

        async def throttled_task_wrapper(*args, **kwargs):
            async with self.can_task_be_executed:
                await self.can_task_be_executed.wait()
            return await coroutine

        return throttled_task_wrapper()

    def _mark_task_done(self, callback) -> Callable:
        """Decorator for callback to set the task as done after the callback is processed."""

        def task_done_wrapper(task: Coroutine) -> None:
            try:
                task_result = task.result()  # type: ignore
            except Exception:
                traceback.print_exc()
            else:
                try:
                    callback(task_result)
                except Exception:
                    traceback.print_exc()
            self.running_tasks.discard(task)

        return task_done_wrapper

    def _run_event_loop(self) -> None:
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
