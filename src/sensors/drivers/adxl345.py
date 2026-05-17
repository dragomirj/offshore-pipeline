# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] ADXL345 Sensor Driver
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <13-May-2026>
# *****************************************************************************
from src.sensors.interrupt_sensor import InterruptSensor

class ADXL345Sensor(InterruptSensor):
    """
    Hardware driver stub for the ADXL345 3-axis accelerometer.
    Channels : vibration_g (g-force)
    """

    REQUIRED_PARAMS: frozenset[str] = frozenset({"cs_pin", "interrupt_pin"})

    def __init__(self, device_id: str, sensor_id: str, warmup_seconds: float, cs_pin: int, interrupt_pin: int):
        super().__init__(device_id, sensor_id, warmup_seconds)
        self._cs_pin        = cs_pin
        self._interrupt_pin = interrupt_pin

    async def _setup(self) -> None:
        raise NotImplementedError(
            "ADXL345Sensor._setup() not implemented. Use a simulated sensor class or provide a hardware-specific implementation."
        )

    async def close(self) -> None:
        pass
