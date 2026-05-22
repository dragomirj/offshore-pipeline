# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] Base Sensor Class
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <12-Feb-2026>
# *****************************************************************************
import asyncio
from abc import ABC, abstractmethod
from src.common.models.sensor_reading import SensorReading

class SensorReadError(Exception):
    """Raised when a sensor read fails due to timeout or calling read() before initialize()."""
    pass

def validate_alert_thresholds(sensor_id: str, alert_thresholds: dict[str, float], required: frozenset[str]) -> None:
    missing = required - alert_thresholds.keys()
    if missing:
        raise ValueError(
            f"Sensor '{sensor_id}' is missing required alert threshold(s): {', '.join(sorted(missing))}. "
            "Add the missing value(s) to alert_thresholds in the device config."
        )

class Sensor(ABC):
    """
    Abstract base class for all physical hardware sensor drivers.
    See: /src/sensors/polled_sensor.py, /src/sensors/interrupt_sensor.py
    """

    REQUIRED_PARAMS: frozenset[str] = frozenset()  # override in subclasses to declare required config parameters

    def __init__(self, device_id: str, sensor_id: str, warmup_seconds: float, alert_thresholds: dict[str, float]):
        self.device_id         = device_id
        self.sensor_id         = sensor_id
        self._warmup           = warmup_seconds
        self._alert_thresholds = alert_thresholds
        self._ready            = False

    async def initialize(self) -> None:
        try:
            await self._setup()
            if self._warmup > 0:
                await asyncio.sleep(self._warmup)
            self._ready = True
        except Exception:
            await self.close()
            raise

    @abstractmethod
    async def _setup(self) -> None: ...

    @abstractmethod
    async def read(self) -> list[SensorReading]: ...

    @abstractmethod
    async def close(self) -> None:  # pragma: no cover
        """Optional cleanup method for hardware drivers. Called on shutdown and on failed initialization."""
        pass

    @property
    def is_ready(self) -> bool:
        return self._ready