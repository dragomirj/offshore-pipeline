# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] Interrupt Sensor Base Class
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <12-Feb-2026>
# *****************************************************************************
import asyncio
from src.sensors.base import Sensor
from src.common.models.sensor_reading import SensorReading
from src.sensors.constants import INTERRUPT_SENSOR_MAX_QUEUE_SIZE

class InterruptSensor(Sensor):
    """
    Base for sensors that push data rather than being polled.
    """

    def __init__(self, device_id: str, sensor_id: str, warmup_seconds: float):
        super().__init__(device_id, sensor_id, warmup_seconds)
        self._queue: asyncio.Queue[list[SensorReading]] = asyncio.Queue(maxsize=INTERRUPT_SENSOR_MAX_QUEUE_SIZE)

    async def read(self) -> list[SensorReading]:
        return await self._queue.get()

    def _on_interrupt(self, readings: list[SensorReading]) -> None:
        try:
            self._queue.put_nowait(readings)
        except asyncio.QueueFull:
            pass  # Older events have priority for ordered processing