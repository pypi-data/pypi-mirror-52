# cython: language_level=3
#  Drakkar-Software OctoBot-Channels
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import asyncio
from asyncio import Queue, CancelledError

from octobot_commons.logging.logging_util import get_logger

from octobot_channels import CONSUMER_CALLBACK_TYPE

"""
A channel Consumer
"""


class Consumer:
    def __init__(self, callback: CONSUMER_CALLBACK_TYPE, size: int = 0, filter_size: bool = False):
        self.logger = get_logger(self.__class__.__name__)

        # Consumer data queue. It contains producer's work (received through Producer.send()).
        self.queue = Queue(maxsize=size)

        # Method to be called when performing task is done
        self.callback = callback

        # Should only be used with .cancel()
        self.consume_task = None

        """
        Should be used as the perform while loop condition
            while(self.should_stop):
                ...
        """
        self.should_stop = False

        """
        TODO
        Filter consumer performing task by waiting for a specified queue size
        """
        self.filter_size = filter_size

    async def consume(self):
        """
        Should be overwritten with a self.queue.get() in a while loop
        :return: None
        """
        while not self.should_stop:
            try:
                await self.callback(**(await self.queue.get()))
            except Exception as e:
                self.logger.exception(f"Exception when calling callback : {e}")

    async def start(self):
        """
        Should be implemented for consumer's non-triggered tasks
        :return: None
        """
        self.should_stop = False

    async def stop(self):
        """
        Stops non-triggered tasks management
        :return: None
        """
        self.should_stop = True
        if self.consume_task:
            self.consume_task.cancel()

    def create_task(self):
        """
        Creates a new asyncio task that contains start() execution
        :return: None
        """
        self.consume_task = asyncio.create_task(self.consume())

    async def run(self):
        """
        - Initialize the consumer
        - Start the consumer main task
        :return: None
        """
        await self.start()
        self.create_task()


class InternalConsumer(Consumer):
    def __init__(self):
        super().__init__(None)

        # Method to be called when performing task is done
        self.callback = self.perform

    async def perform(self, **kwargs):
        raise NotImplementedError("perform is not implemented")


class SupervisedConsumer(Consumer):
    async def consume(self):
        """
        Can be overwritten with a while loop that contains :
        - self.queue.get()
        - finally: self.queue.task_done()
        :return: None
        """
        while not self.should_stop:
            try:
                await self.callback(**(await self.queue.get()))
            except Exception as e:
                self.logger.exception(f"Exception when calling callback : {e}")
            finally:
                try:
                    self.queue.task_done()
                except ValueError:  # when task_done() is called when the Exception was CancelledError
                    pass
