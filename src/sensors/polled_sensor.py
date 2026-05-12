# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] Polled Sensor Base Class
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <12-Feb-2026>
# *****************************************************************************
import asyncio
from abc import abstractmethod
from src.sensors.base import Sensor, SensorReadError
from src.common.models.sensor_reading import SensorReading
from src.sensors.constants import POLLED_SENSOR_READ_TIMEOUT

class PolledSensor(Sensor):
    """
    Base for sensors that require polling to get data.
    """

    def __init__(self, device_id: str, sensor_id: str, warmup_seconds: float):
        super().__init__(device_id, sensor_id, warmup_seconds)

    async def read(self) -> list[SensorReading]:
        if not self._ready:
            raise SensorReadError(f"{self.sensor_id} not initialized.")
        try:
            return await asyncio.wait_for(self._read_hardware(), timeout=POLLED_SENSOR_READ_TIMEOUT)
        except asyncio.TimeoutError:
            raise SensorReadError(f"{self.sensor_id} timed out.")

    @abstractmethod
    async def _read_hardware(self) -> list[SensorReading]: ...

    @property
    def blocks_on_read(self) -> bool:
        return True