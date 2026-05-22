# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] Base Sensor Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <07-May-2026>
# *****************************************************************************
import pytest
from unittest.mock import AsyncMock, patch
from src.common.models.sensor_reading import SensorReading
from src.sensors.base import Sensor, validate_alert_thresholds

DUMMY_DEVICE_ID = "dummyDeviceId"
DUMMY_SENSOR_ID = "dummySensorId"
WARMUP_OF_0_SECONDS = 0.0
WARMUP_OF_5_SECONDS = 5.0

class DummySensor(Sensor):
    def __init__(self, warmup_seconds: float = WARMUP_OF_0_SECONDS, setup_failed: bool = False):
        super().__init__(DUMMY_DEVICE_ID, DUMMY_SENSOR_ID, warmup_seconds, {})
        self.setup_failed = setup_failed
        self.setup_called = False
        self.close_called = False

    async def _setup(self) -> None:
        self.setup_called = True
        if self.setup_failed:
            raise RuntimeError("setup failed")

    async def read(self) -> list[SensorReading]:  # pragma: no cover
        return []

    async def close(self) -> None:
        self.close_called = True

def test_validate_alert_thresholds_passes_when_all_present():
    validate_alert_thresholds(DUMMY_SENSOR_ID, {"temperature_c": 1000.0, "humidity_rh": 50.0}, frozenset({"temperature_c", "humidity_rh"}))

def test_validate_alert_thresholds_raises_on_single_missing():
    with pytest.raises(ValueError, match="Sensor '" + DUMMY_SENSOR_ID + "'.*temperature_c"):
        validate_alert_thresholds(DUMMY_SENSOR_ID, {}, frozenset({"temperature_c"}))

def test_validate_alert_thresholds_raises_on_multiple_missing():
    with pytest.raises(ValueError, match="humidity_rh, temperature_c"):
        validate_alert_thresholds(DUMMY_SENSOR_ID, {}, frozenset({"temperature_c", "humidity_rh"}))

@pytest.mark.asyncio
async def test_initialize_success_sets_ready():
    sensor = DummySensor()
    await sensor.initialize()

    assert sensor.setup_called is True
    assert sensor.close_called is False
    assert sensor.is_ready is True

@pytest.mark.asyncio
async def test_initialize_failure_calls_close_and_reraises():
    sensor = DummySensor(setup_failed=True)
    with pytest.raises(RuntimeError, match="setup failed"):
        await sensor.initialize()

    assert sensor.setup_called is True
    assert sensor.close_called is True
    assert sensor.is_ready is False

@pytest.mark.asyncio
async def test_initialize_waits_for_warmup():
    sensor = DummySensor(warmup_seconds=WARMUP_OF_5_SECONDS)
    with patch("asyncio.sleep", new_callable=AsyncMock) as sleep_mock:
        await sensor.initialize()

    sleep_mock.assert_awaited_once_with(WARMUP_OF_5_SECONDS)

@pytest.mark.asyncio
async def test_initialize_skips_sleep_when_no_warmup():
    sensor = DummySensor()
    with patch("asyncio.sleep", new_callable=AsyncMock) as sleep_mock:
        await sensor.initialize()

    sleep_mock.assert_not_awaited()