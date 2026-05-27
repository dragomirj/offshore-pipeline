# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] Sensor Factory Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <29-Apr-2026>
# *****************************************************************************
import pytest
from typing import Any
from src.common.models.sensor_reading import SensorReading
from src.config import SensorConfig
from src.sensors.base import Sensor
from src.sensors.factory import (
    SensorFactory,
    SensorConfigError,
    SensorNotRegisteredError,
)
from src.common.enums.sensor_type import SensorType

DUMMY_DEVICE_ID     = "dummyDeviceId"
DUMMY_SENSOR_ID_1   = "dummySensorId1"
DUMMY_SENSOR_ID_2   = "dummySensorId2"
DUMMY_SENSOR_TYPE   = SensorType.BME280
WARMUP_OF_5_SECONDS = 5.0

class DummySensor(Sensor):
    REQUIRED_PARAMS = frozenset({"dummy_param"})

    def __init__(self, device_id: str, sensor_id: str, warmup_seconds: float, alert_thresholds: dict[str, float], **params: Any):
        super().__init__(device_id, sensor_id, warmup_seconds, alert_thresholds)
        self.params = params

    async def _setup(self) -> None:  # pragma: no cover
        pass

    async def read(self) -> list[SensorReading]:  # pragma: no cover
        return []

    async def close(self) -> None:  # pragma: no cover
        pass

    @property
    def blocks_on_read(self) -> bool:
        return False

def _make_config(
    sensor_id: str = DUMMY_SENSOR_ID_1,
    warmup_seconds: float = 0.0,
    params: dict[str, Any] | None = None,
) -> SensorConfig:
    return SensorConfig(
        sensor_id=sensor_id,
        sensor_type=str(DUMMY_SENSOR_TYPE),
        poll_interval_seconds=1.0,
        warmup_seconds=warmup_seconds,
        enabled=True,
        alert_thresholds={},
        params=params if params is not None else {},
    )

@pytest.fixture
def registry(monkeypatch: pytest.MonkeyPatch):
    # Replace global registry with a controlled test mapping
    monkeypatch.setattr(
        SensorFactory,
        "_registry",
        {DUMMY_SENSOR_TYPE: DummySensor},
    )

def test_create_returns_sensor_with_default_warmup(registry: pytest.MonkeyPatch):
    sensor = SensorFactory.create(DUMMY_DEVICE_ID, _make_config(params={"dummy_param": 1}))

    assert sensor.device_id == DUMMY_DEVICE_ID
    assert sensor.sensor_id == DUMMY_SENSOR_ID_1
    assert sensor._warmup == 0.0  # pyright: ignore[reportPrivateUsage]
    assert sensor.params["dummy_param"] == 1  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]

def test_create_respects_custom_warmup(registry: pytest.MonkeyPatch):
    sensor = SensorFactory.create(
        DUMMY_DEVICE_ID,
        _make_config(warmup_seconds=WARMUP_OF_5_SECONDS, params={"dummy_param": 1}),
    )

    assert sensor._warmup == WARMUP_OF_5_SECONDS  # pyright: ignore[reportPrivateUsage]

def test_create_raises_when_required_params_missing(registry: pytest.MonkeyPatch):
    with pytest.raises(SensorConfigError) as exc:
        SensorFactory.create(DUMMY_DEVICE_ID, _make_config(params={}))

    assert "missing required params" in str(exc.value)

def test_create_raises_for_unregistered_sensor(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(SensorFactory, "_registry", {})

    with pytest.raises(SensorNotRegisteredError) as exc:
        SensorFactory.create(DUMMY_DEVICE_ID, _make_config(params={"dummy_param": 1}))

    assert "not registered" in str(exc.value)

def test_get_sensor_class_returns_registered_class(registry: pytest.MonkeyPatch):
    sensor_class = SensorFactory.get_sensor_class(DUMMY_SENSOR_TYPE)

    assert sensor_class is DummySensor

def test_get_sensor_class_raises_for_unregistered(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(SensorFactory, "_registry", {})

    with pytest.raises(SensorNotRegisteredError):
        SensorFactory.get_sensor_class(DUMMY_SENSOR_TYPE)
