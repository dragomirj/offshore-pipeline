# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Readable Protocol
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <13-Feb-2026>
# ***************************************************************************** 
from typing import Protocol, runtime_checkable
from src.common.models.sensor_reading import SensorReading

@runtime_checkable
class Readable(Protocol):
    """
    Asynchronous source of SensorReading data.
    Lets consumers (e.g., pollers) use real or simulated sensors interchangeably.
    """
    
    async def initialize(self) -> None: ...
    async def read(self) -> list[SensorReading]: ...
    async def close(self) -> None: ...

    @property
    def blocks_on_read(self) -> bool:
        """
        True if read() blocks internally until an event arrives (interrupt sensors).
        False if read() returns immediately and the caller should sleep (polled sensors).
        """
        ...