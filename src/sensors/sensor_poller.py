# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] Sensor Poller
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <13-Feb-2026>
# *****************************************************************************
import asyncio
import logging
from collections.abc import Callable, Awaitable
from src.common.interfaces.readable import Readable
from src.common.models.sensor_reading import SensorReading
from src.sensors.constants import SENSOR_POLLER_BACKOFF_CAP, SENSOR_POLLER_MAX_ERRORS

logger = logging.getLogger(__name__)

class SensorPoller:
    """
    Asynchronously polls a readable sensor or simulator at a specified interval and invokes a callback with the readings.
    """

    def __init__(self, readable: Readable, callback: Callable[[list[SensorReading]], Awaitable[None]], poll_interval: float, max_errors: int = SENSOR_POLLER_MAX_ERRORS):
        self._readable    = readable
        self._callback    = callback
        self._interval    = poll_interval
        self._max_errors  = max_errors
        self._error_count = 0

    async def run(self) -> None:
        await self._readable.initialize()
        try:
            while True:
                try:
                    readings = await self._readable.read()
                    await self._callback(readings)
                except asyncio.CancelledError:
                    raise
                except Exception as e:
                    self._error_count += 1
                    logger.warning(
                        "Sensor read failed - sensor=%s attempt=%d of %d error=%s",
                        getattr(self._readable, "sensor_id", "unknown"),
                        self._error_count,
                        self._max_errors,
                        e,
                    )
                    if self._error_count >= self._max_errors:
                        raise RuntimeError(
                            f"Sensor '{getattr(self._readable, 'sensor_id', 'unknown')}' failed {self._max_errors} consecutive times: {e}"
                        ) from e
                    backoff = min(self._interval * (2 ** self._error_count), SENSOR_POLLER_BACKOFF_CAP)
                    await asyncio.sleep(backoff)
                else:
                    self._error_count = 0
                    if not self._readable.blocks_on_read:
                        await asyncio.sleep(self._interval)
        finally:
            await self._readable.close()