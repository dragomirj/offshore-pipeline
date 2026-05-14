# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] Interrupt Sensor Base Class
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <12-Feb-2026>
# *****************************************************************************
import asyncio
import logging
from src.sensors.base import Sensor
from src.common.models.sensor_reading import SensorReading
from src.sensors.constants import INTERRUPT_SENSOR_MAX_QUEUE_SIZE

logger = logging.getLogger(__name__)

class InterruptSensor(Sensor):
    """
    Base for sensors that push data rather than being polled.

    On a full queue the oldest event is dropped so the newest reading
    always survives. Drops are counted and logged so silent data loss
    is observable upstream.
    """

    def __init__(self, device_id: str, sensor_id: str, warmup_seconds: float):
        super().__init__(device_id, sensor_id, warmup_seconds)
        self._queue: asyncio.Queue[list[SensorReading]] = asyncio.Queue(maxsize=INTERRUPT_SENSOR_MAX_QUEUE_SIZE)
        self._dropped_count = 0

    async def read(self) -> list[SensorReading]:
        return await self._queue.get()

    def _on_interrupt(self, readings: list[SensorReading]) -> None:
        if self._queue.full():
            try:
                self._queue.get_nowait()
            except asyncio.QueueEmpty:  # pragma: no cover
                pass
            
            self._dropped_count += 1
            logger.warning(
                "Interrupt sensor queue is full, oldest reading dropped - sensor=%s total_dropped=%d",
                self.sensor_id, self._dropped_count,
            )
            
        self._queue.put_nowait(readings)

    @property
    def dropped_count(self) -> int:
        return self._dropped_count

    @property
    def blocks_on_read(self) -> bool:
        return True