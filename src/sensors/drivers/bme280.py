# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] BME280 Sensor Driver
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <13-Feb-2026>
# *****************************************************************************
from src.sensors.polled_sensor import PolledSensor
from src.common.models.sensor_reading import SensorReading

class BME280Sensor(PolledSensor):
    """
    Hardware driver stub for the Bosch BME280 environmental sensor.
    Channels : temperature_c (°C) · humidity_rh (% RH) · pressure_hpa (hPa)
    """

    REQUIRED_PARAMS: frozenset[str] = frozenset({"i2c_address"})

    def __init__(self, device_id: str, sensor_id: str, warmup_seconds: float, i2c_address: int = 0x77):
        super().__init__(device_id, sensor_id, warmup_seconds)
        self._i2c_address = i2c_address

    async def _setup(self) -> None:
        raise NotImplementedError(
            "BME280Sensor._setup() not implemented. Use a simulated sensor class or provide a hardware-specific implementation."
        )

    async def _read_hardware(self) -> list[SensorReading]:
        raise NotImplementedError(
            "BME280Sensor._read_hardware() not implemented. Use a simulated sensor class or provide a hardware-specific implementation."
        )
        
    async def close(self) -> None:
        pass