# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] Polled Sensor Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <07-May-2026>
# *****************************************************************************
import pytest
import asyncio
from src.common.models.sensor_reading import SensorReading
from src.sensors.constants import POLLED_SENSOR_READ_TIMEOUT
from src.sensors.polled_sensor import PolledSensor
from src.sensors.polled_sensor import SensorReadError
from tests.utils.sensors import create_dummy_reading

DUMMY_DEVICE_ID = "dummyDeviceId"
DUMMY_SENSOR_ID = "dummySensorId"
WARMUP_OF_0_SECONDS = 0.0

class DummyPolledSensor(PolledSensor):
    def __init__(self, hardware_result: list[SensorReading] | None = None):
        super().__init__(DUMMY_DEVICE_ID, DUMMY_SENSOR_ID, WARMUP_OF_0_SECONDS)
        self.hardware_result: list[SensorReading] = ([] if hardware_result is None else hardware_result)

    async def _setup(self) -> None:  # pragma: no cover
        pass

    async def _read_hardware(self) -> list[SensorReading]:
        return self.hardware_result
    
    async def close(self) -> None:  # pragma: no cover
        pass

@pytest.mark.asyncio
async def test_read_raises_when_not_initialized():
    sensor = DummyPolledSensor()

    with pytest.raises(SensorReadError, match="has not been initialized"):
        await sensor.read()

@pytest.mark.asyncio
async def test_read_returns_hardware_result():
    readings: list[SensorReading] = [create_dummy_reading(55.0)]
    sensor = DummyPolledSensor(hardware_result=readings)
    sensor._ready = True  # pyright: ignore[reportPrivateUsage]
    result = await sensor.read()

    assert result == readings

@pytest.mark.asyncio
async def test_read_converts_timeout_to_sensor_error():
    class SlowPolledSensor(DummyPolledSensor):
        async def _read_hardware(self) -> list[SensorReading]:
            await asyncio.sleep(POLLED_SENSOR_READ_TIMEOUT + 1)
            return []  # pragma: no cover

    sensor = SlowPolledSensor()
    sensor._ready = True  # pyright: ignore[reportPrivateUsage]

    with pytest.raises(SensorReadError, match="timed out"):
        await sensor.read()

def test_blocks_on_read_is_false():
    sensor = DummyPolledSensor()
    assert sensor.blocks_on_read is False