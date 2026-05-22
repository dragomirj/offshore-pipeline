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

@pytest.fixture
def registry(monkeypatch: pytest.MonkeyPatch):
    # Replace global registry with a controlled test mapping
    monkeypatch.setattr(
        SensorFactory,
        "_registry",
        {DUMMY_SENSOR_TYPE: DummySensor},
    )

def test_create_returns_sensor_with_default_warmup(registry: pytest.MonkeyPatch):
    config = {"params": {"dummy_param": 1}}

    sensor = SensorFactory.create(
        DUMMY_DEVICE_ID,
        DUMMY_SENSOR_ID_1,
        DUMMY_SENSOR_TYPE,
        config,
    )

    assert sensor.device_id == DUMMY_DEVICE_ID
    assert sensor.sensor_id == DUMMY_SENSOR_ID_1
    assert sensor._warmup == 0.0  # pyright: ignore[reportPrivateUsage]
    assert sensor.params["dummy_param"] == 1  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]

def test_create_respects_custom_warmup(registry: pytest.MonkeyPatch):
    config = {"warmup_seconds": WARMUP_OF_5_SECONDS, "params": {"dummy_param": 1}}

    sensor = SensorFactory.create(
        DUMMY_DEVICE_ID,
        DUMMY_SENSOR_ID_1,
        DUMMY_SENSOR_TYPE,
        config,
    )

    assert sensor._warmup == WARMUP_OF_5_SECONDS  # pyright: ignore[reportPrivateUsage]

def test_create_raises_when_required_params_missing(registry: pytest.MonkeyPatch):
    config = {"params": {}}  # pyright: ignore[reportUnknownVariableType]

    with pytest.raises(SensorConfigError) as exc:
        SensorFactory.create(
            DUMMY_DEVICE_ID,
            DUMMY_SENSOR_ID_1,
            DUMMY_SENSOR_TYPE,
            config,  # pyright: ignore[reportUnknownArgumentType]
        )

    assert "missing required params" in str(exc.value)

def test_create_raises_for_unregistered_sensor(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(SensorFactory, "_registry", {})

    with pytest.raises(SensorNotRegisteredError) as exc:
        SensorFactory.create(
            DUMMY_DEVICE_ID,
            DUMMY_SENSOR_ID_1,
            DUMMY_SENSOR_TYPE,
            {"params": {"dummy_param": 1}},
        )

    assert "not registered" in str(exc.value)

def test_create_all_returns_single_sensor(registry: pytest.MonkeyPatch):
    configs = [{
        "sensor_id": DUMMY_SENSOR_ID_1,
        "sensor_type": str(DUMMY_SENSOR_TYPE),
        "enabled": True,
        "params": {"dummy_param": 1},
    }]

    sensors = SensorFactory.create_all(DUMMY_DEVICE_ID, configs)

    assert len(sensors) == 1
    assert sensors[0].sensor_id == DUMMY_SENSOR_ID_1

def test_create_all_returns_multiple_sensors(registry: pytest.MonkeyPatch):
    configs = [
        {
            "sensor_id": DUMMY_SENSOR_ID_1,
            "sensor_type": str(DUMMY_SENSOR_TYPE),
            "enabled": True,
            "params": {"dummy_param": 1},
        },
        {
            "sensor_id": DUMMY_SENSOR_ID_2,
            "sensor_type": str(DUMMY_SENSOR_TYPE),
            "enabled": True,
            "params": {"dummy_param": 2},
        },
    ]

    sensors = SensorFactory.create_all(DUMMY_DEVICE_ID, configs)

    assert len(sensors) == 2
    assert {s.sensor_id for s in sensors} == {DUMMY_SENSOR_ID_1, DUMMY_SENSOR_ID_2}

def test_create_all_skips_disabled_sensors(registry: pytest.MonkeyPatch):
    configs = [{
        "sensor_id": DUMMY_SENSOR_ID_1,
        "sensor_type": str(DUMMY_SENSOR_TYPE),
        "enabled": False,
        "params": {"dummy_param": 1},
    }]

    sensors = SensorFactory.create_all(DUMMY_DEVICE_ID, configs)

    assert sensors == []

def test_create_all_raises_when_sensor_id_missing():
    configs = [{
        "sensor_type": str(DUMMY_SENSOR_TYPE),
        "enabled": True,
        "params": {"dummy_param": 1},
    }]

    with pytest.raises(SensorConfigError) as exc:
        SensorFactory.create_all(DUMMY_DEVICE_ID, configs)

    assert "missing the required 'sensor_id' field" in str(exc.value)

def test_create_all_raises_when_sensor_type_missing():
    configs = [{
        "sensor_id": DUMMY_SENSOR_ID_1,
        "enabled": True,
        "params": {"dummy_param": 1},
    }]

    with pytest.raises(SensorConfigError) as exc:
        SensorFactory.create_all(DUMMY_DEVICE_ID, configs)

    assert "missing the required 'sensor_type' field" in str(exc.value)

def test_create_all_raises_when_params_missing():
    configs = [{
        "sensor_id": DUMMY_SENSOR_ID_1,
        "sensor_type": str(DUMMY_SENSOR_TYPE),
        "enabled": True,
    }]

    with pytest.raises(SensorConfigError) as exc:
        SensorFactory.create_all(DUMMY_DEVICE_ID, configs)

    assert "missing required params" in str(exc.value)

def test_create_all_raises_for_invalid_sensor_type():
    configs = [{
        "sensor_id": DUMMY_SENSOR_ID_1,
        "sensor_type": "invalid_type",
        "enabled": True,
        "params": {"dummy_param": 1},
    }]

    with pytest.raises(SensorConfigError) as exc:
        SensorFactory.create_all(DUMMY_DEVICE_ID, configs)

    assert "invalid" in str(exc.value).lower()

def test_create_all_raises_when_required_params_missing(registry: pytest.MonkeyPatch):
    configs = [{  # pyright: ignore[reportUnknownVariableType]
        "sensor_id": DUMMY_SENSOR_ID_1,
        "sensor_type": str(DUMMY_SENSOR_TYPE),
        "enabled": True,
        "params": {},
    }]

    with pytest.raises(SensorConfigError) as exc:
        SensorFactory.create_all(DUMMY_DEVICE_ID, configs)  # pyright: ignore[reportUnknownArgumentType]

    assert "missing required params" in str(exc.value)

def test_create_all_aggregates_multiple_errors():
    # Multiple invalid configs should be reported in a single aggregated error
    configs = [
        {"enabled": True},
        {"sensor_id": DUMMY_SENSOR_ID_2, "enabled": True},
    ]

    with pytest.raises(SensorConfigError) as exc:
        SensorFactory.create_all(DUMMY_DEVICE_ID, configs)

    message = str(exc.value)

    assert "2 configuration error(s)" in message
    assert "[1]" in message
    assert "[2]" in message

def test_get_sensor_class_returns_registered_class(registry: pytest.MonkeyPatch):
    sensor_class = SensorFactory.get_sensor_class(DUMMY_SENSOR_TYPE)

    assert sensor_class is DummySensor

def test_get_sensor_class_raises_for_unregistered(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(SensorFactory, "_registry", {})

    with pytest.raises(SensorNotRegisteredError):
        SensorFactory.get_sensor_class(DUMMY_SENSOR_TYPE)