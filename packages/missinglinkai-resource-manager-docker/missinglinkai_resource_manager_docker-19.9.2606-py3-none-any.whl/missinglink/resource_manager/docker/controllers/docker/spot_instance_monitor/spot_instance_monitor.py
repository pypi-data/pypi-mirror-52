import logging
import asyncio
import abc

from missinglink.resource_manager.docker.sync_async_tools import run_blocking_code_in_thread

logger = logging.getLogger(__name__)


class SpotInstanceMonitor:

    SLEEP_TIME = 30
    STEP_NAME = 'Monitor'

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return await run_blocking_code_in_thread(self.check_termination_time, logger=logger,
                                                     loop=asyncio.get_event_loop())
        except StopIteration:
            raise StopAsyncIteration

    async def wait(self):
        await asyncio.sleep(self.SLEEP_TIME)

    @abc.abstractmethod
    def check_termination_time(self):
        """
        """
