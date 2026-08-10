import asyncio
import logging
import os
import time
from typing import Awaitable, Callable

logger = logging.getLogger(__name__)

JOB_TIMEOUT_SECONDS = 60
# Generous margin beyond JOB_TIMEOUT_SECONDS: some hangs (e.g. a poisoned
# aiohttp connection pool after a network blip) don't respect asyncio
# cancellation and can wedge the worker even past its own wait_for timeout.
# When that happens there is no in-process fix — hard-exit and let Docker's
# restart policy bring up a fresh process (fresh connection pool, fresh
# scheduler) instead of requiring a manual SSH intervention.
WATCHDOG_TIMEOUT_SECONDS = 180
WATCHDOG_POLL_SECONDS = 30


class SingleWriterQueue:
    """Serializes async jobs through one worker task.

    This is what guarantees no races on the state store / canvas render:
    every state mutation + canvas re-render must be submitted as a single
    job here rather than awaited directly from a request handler.
    """

    def __init__(self):
        self._queue: asyncio.Queue[tuple[Callable[[], Awaitable], asyncio.Future]] = asyncio.Queue()
        self._worker_task: asyncio.Task | None = None
        self._watchdog_task: asyncio.Task | None = None
        self._last_job_started = time.monotonic()
        self._processing = False

    def start(self) -> None:
        if self._worker_task is None:
            self._worker_task = asyncio.create_task(self._run())
        if self._watchdog_task is None:
            self._watchdog_task = asyncio.create_task(self._watchdog())

    async def _run(self) -> None:
        while True:
            job, future = await self._queue.get()
            self._last_job_started = time.monotonic()
            self._processing = True
            try:
                # A hung network call here (e.g. Slack API) would otherwise
                # wedge this single worker forever, since every job — including
                # the daily cleanup — is serialized through it.
                result = await asyncio.wait_for(job(), timeout=JOB_TIMEOUT_SECONDS)
                if not future.done():
                    future.set_result(result)
            except Exception as exc:  # noqa: BLE001 - propagate to caller, keep worker alive
                if not future.done():
                    future.set_exception(exc)
            finally:
                self._processing = False
                self._queue.task_done()

    async def _watchdog(self) -> None:
        while True:
            await asyncio.sleep(WATCHDOG_POLL_SECONDS)
            stuck_for = time.monotonic() - self._last_job_started
            if self._processing and stuck_for > WATCHDOG_TIMEOUT_SECONDS:
                logger.critical(
                    "Queue worker stuck for %.0fs on a single job (past its own %ds timeout) — "
                    "forcing process exit for a clean restart",
                    stuck_for,
                    JOB_TIMEOUT_SECONDS,
                )
                os._exit(1)

    async def submit(self, job: Callable[[], Awaitable]):
        future: asyncio.Future = asyncio.get_event_loop().create_future()
        await self._queue.put((job, future))
        return await future
