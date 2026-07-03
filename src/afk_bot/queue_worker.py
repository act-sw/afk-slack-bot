import asyncio
from typing import Awaitable, Callable


class SingleWriterQueue:
    """Serializes async jobs through one worker task.

    This is what guarantees no races on the state store / canvas render:
    every state mutation + canvas re-render must be submitted as a single
    job here rather than awaited directly from a request handler.
    """

    def __init__(self):
        self._queue: asyncio.Queue[tuple[Callable[[], Awaitable], asyncio.Future]] = asyncio.Queue()
        self._worker_task: asyncio.Task | None = None

    def start(self) -> None:
        if self._worker_task is None:
            self._worker_task = asyncio.create_task(self._run())

    async def _run(self) -> None:
        while True:
            job, future = await self._queue.get()
            try:
                result = await job()
                if not future.done():
                    future.set_result(result)
            except Exception as exc:  # noqa: BLE001 - propagate to caller, keep worker alive
                if not future.done():
                    future.set_exception(exc)
            finally:
                self._queue.task_done()

    async def submit(self, job: Callable[[], Awaitable]):
        future: asyncio.Future = asyncio.get_event_loop().create_future()
        await self._queue.put((job, future))
        return await future
