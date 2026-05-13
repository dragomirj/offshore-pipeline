# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] MQ135 Sensor Driver
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <13-Feb-2026>
# *****************************************************************************
from src.sensors.polled_sensor import PolledSensor
from src.common.models.sensor_reading import SensorReading

class MQ135Sensor(PolledSensor):
    """
    Hardware driver stub for the MQ135 air quality sensor.
    Channels : co2_ppm (PPM - inferred) · nh3_ppm (PPM)
    """

    REQUIRED_PARAMS: frozenset[str] = frozenset({"adc_channel"})

    def __init__(self, device_id: str, sensor_id: str, warmup_seconds: float, adc_channel: int):
        super().__init__(device_id, sensor_id, warmup_seconds)
        self._adc_channel = adc_channel

    async def _setup(self) -> None:
        raise NotImplementedError(
            "MQ135Sensor._setup() not implemented. Use a simulated sensor class or provide a hardware-specific implementation."
        )

    async def _read_hardware(self) -> list[SensorReading]:
        raise NotImplementedError(
            "MQ135Sensor._read_hardware() not implemented. Use a simulated sensor class or provide a hardware-specific implementation."
        )
        
    async def close(self) -> None:
        pass