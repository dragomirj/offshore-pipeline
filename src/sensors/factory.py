# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] Sensor Factory
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <13-Feb-2026>
# *****************************************************************************
from __future__ import annotations
from typing import Any
from src.common.enums.sensor_type import SensorType
from src.sensors.base import Sensor
from src.sensors.registry import SENSOR_REGISTRY

class SensorNotRegisteredError(Exception):
    """Raised when a sensor type is not present in the registry."""

class SensorConfigError(Exception):
    """Raised when sensor configuration is invalid."""

class SensorFactory:
    _registry: dict[SensorType, type[Sensor]] = dict(SENSOR_REGISTRY)

    @classmethod
    def create(cls, device_id: str, sensor_id: str, sensor_type: SensorType, config: dict[str, Any]) -> Sensor:
        try:
            sensor_class = cls._registry[sensor_type]
        except KeyError:
            raise SensorNotRegisteredError(
                f"Sensor type '{sensor_type}' is not registered. Known types: {', '.join(str(t) for t in cls._registry)}."
            ) from None

        params = config.get("params", {})  # sensors with no REQUIRED_PARAMS don't need a params key in YAML
        missing = sensor_class.REQUIRED_PARAMS - params.keys()

        if missing:
            raise SensorConfigError(
                f"Sensor '{sensor_id}' of type '{sensor_type}' is missing required params: {', '.join(sorted(missing))}."
            )

        return sensor_class(
            device_id=device_id,
            sensor_id=sensor_id,
            warmup_seconds=config.get("warmup_seconds", 0.0),
            alert_thresholds=config.get("alert_thresholds", {}),
            **params,
        )

    @classmethod
    def create_all(cls, device_id: str, sensor_configs: list[dict[str, Any]]) -> list[Sensor]:
        sensors: list[Sensor] = []
        errors: list[str] = []

        for cfg in sensor_configs:
            if not cfg.get("enabled", False):
                continue

            sensor_id = cfg.get("sensor_id")
            if not sensor_id:
                errors.append("A sensor config entry is missing the required 'sensor_id' field.")
                continue

            sensor_type_raw = cfg.get("sensor_type")
            if not sensor_type_raw:
                errors.append(f"Sensor '{sensor_id}' is missing the required 'sensor_type' field.")
                continue

            try:
                sensor_type = SensorType.parse(sensor_type_raw)
                sensors.append(cls.create(device_id, sensor_id, sensor_type, cfg))
            except (ValueError, SensorNotRegisteredError, SensorConfigError) as e:
                errors.append(str(e))

        if errors:
            raise SensorConfigError(
                f"Device '{device_id}' has {len(errors)} configuration error(s):\n"
                + "\n".join(f"  [{i + 1}] {err}" for i, err in enumerate(errors))
            )

        return sensors

    @classmethod
    def get_sensor_class(cls, sensor_type: SensorType) -> type[Sensor]:
        try:
            return cls._registry[sensor_type]
        except KeyError:
            raise SensorNotRegisteredError(
                f"Sensor type '{sensor_type}' is not registered."
            ) from None