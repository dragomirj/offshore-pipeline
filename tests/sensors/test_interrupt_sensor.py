# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] Interrupt Sensor Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <07-May-2026>
# *****************************************************************************
import pytest
from src.common.models.sensor_reading import SensorReading
from src.sensors.constants import INTERRUPT_SENSOR_MAX_QUEUE_SIZE
from src.sensors.interrupt_sensor import InterruptSensor
from tests.utils.sensors import create_dummy_reading

DUMMY_DEVICE_ID = "dummyDeviceId"
DUMMY_SENSOR_ID = "dummySensorId"
WARMUP_OF_0_SECONDS = 0.0

class DummyInterruptSensor(InterruptSensor):
    def __init__(self):
        super().__init__(DUMMY_DEVICE_ID, DUMMY_SENSOR_ID, WARMUP_OF_0_SECONDS, {})

    async def _setup(self) -> None:  # pragma: no cover
        pass

    async def close(self) -> None:  # pragma: no cover
        pass

@pytest.mark.asyncio
async def test_read_returns_interrupt_data():
    readings: list[SensorReading] = [create_dummy_reading(55.0)]
    sensor = DummyInterruptSensor()
    sensor._on_interrupt(readings)  # pyright: ignore[reportPrivateUsage]
    result = await sensor.read()

    assert result == readings

@pytest.mark.asyncio
async def test_interrupt_queue_preserves_order():
    readings_1: list[SensorReading] = [create_dummy_reading(1.0)]
    readings_2: list[SensorReading] = [create_dummy_reading(2.0)]
    sensor = DummyInterruptSensor()
    sensor._on_interrupt(readings_1)  # pyright: ignore[reportPrivateUsage]
    sensor._on_interrupt(readings_2)  # pyright: ignore[reportPrivateUsage]

    assert await sensor.read() == readings_1
    assert await sensor.read() == readings_2

@pytest.mark.asyncio
async def test_queue_full_drops_oldest_event():
    sensor = DummyInterruptSensor()
    queued_readings: list[list[SensorReading]] = [
        [create_dummy_reading(float(i))]
        for i in range(INTERRUPT_SENSOR_MAX_QUEUE_SIZE)
    ]

    for readings in queued_readings:
        sensor._on_interrupt(readings)  # pyright: ignore[reportPrivateUsage]

    newest_readings: list[SensorReading] = [create_dummy_reading(-999.0), create_dummy_reading(-993.0)]
    sensor._on_interrupt(newest_readings)  # pyright: ignore[reportPrivateUsage]

    assert sensor.dropped_count == 1

    results: list[list[SensorReading]] = []
    for _ in range(INTERRUPT_SENSOR_MAX_QUEUE_SIZE):
        results.append(await sensor.read())

    assert queued_readings[0] not in results
    assert newest_readings in results

def test_blocks_on_read_is_true():
    sensor = DummyInterruptSensor()
    assert sensor.blocks_on_read is True