# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] SCD40 Sensor Driver
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <13-Feb-2026>
# *****************************************************************************
from src.sensors.polled_sensor import PolledSensor
from src.common.models.sensor_reading import SensorReading

class SCD40Sensor(PolledSensor):
    """
    Hardware driver stub for the Sensirion SCD40 CO2 sensor.
    Channels : co2_ppm (PPM) · temperature_c (°C) · humidity_rh (% RH)
    """

    REQUIRED_PARAMS: frozenset[str] = frozenset()

    def __init__(self, device_id: str, sensor_id: str, warmup_seconds: float):
        super().__init__(device_id, sensor_id, warmup_seconds)
        self._i2c_address = 0x62  # I2C address is hardwired to 0x62

    async def _setup(self) -> None:
        raise NotImplementedError(
            "SCD40Sensor._setup() not implemented. Use a simulated sensor class or provide a hardware-specific implementation."
        )

    async def _read_hardware(self) -> list[SensorReading]:
        raise NotImplementedError(
            "SCD40Sensor._read_hardware() not implemented. Use a simulated sensor class or provide a hardware-specific implementation."
        )
        
    async def close(self) -> None:
        pass