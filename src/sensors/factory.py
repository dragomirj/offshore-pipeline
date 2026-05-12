# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] Sensor Factory
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <13-Feb-2026>
# *****************************************************************************
from __future__ import annotations
from typing import Any, Type
from src.common.enums.sensor_type import SensorType
from src.sensors.base import Sensor
from src.sensors.registry import SENSOR_REGISTRY

class SensorNotRegisteredError(Exception):
    """Raised when a sensor type is not present in the registry."""

class SensorConfigError(Exception):
    """Raised when sensor configuration is invalid."""

class SensorFactory:
    _registry: dict[SensorType, Type[Sensor]] = dict(SENSOR_REGISTRY)

    @classmethod
    def create(cls, device_id: str, sensor_id: str, sensor_type: SensorType, config: dict[str, Any]) -> Sensor:
        try:
            sensor_class = cls._registry[sensor_type]
        except KeyError:
            raise SensorNotRegisteredError(
                f"Sensor type '{sensor_type}' is not registered. "
                f"Known types: {[str(t) for t in cls._registry]}."
            ) from None

        params = config.get("params", {})
        missing = sensor_class.REQUIRED_PARAMS - params.keys()

        if missing:
            raise SensorConfigError(
                f"Sensor '{sensor_id}' (type='{sensor_type}') "
                f"missing required params: {sorted(missing)}."
            )

        return sensor_class(
            device_id=device_id,
            sensor_id=sensor_id,
            warmup_seconds=config.get("warmup_seconds", 0.0),
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
                errors.append(f"Missing 'sensor_id': {cfg}")
                continue

            sensor_type_from_cfg = cfg.get("sensor_type")
            if not sensor_type_from_cfg:
                errors.append(f"{sensor_id}: missing 'sensor_type'")
                continue

            if "params" not in cfg:
                errors.append(f"{sensor_id}: missing 'params'")
                continue

            try:
                sensor_type = SensorType.parse(sensor_type_from_cfg)
                sensors.append(
                    cls.create(device_id, sensor_id, sensor_type, cfg)
                )
            except (KeyError, ValueError, SensorNotRegisteredError, SensorConfigError) as e:
                errors.append(f"{sensor_id}: {e}")

        if errors:
            raise SensorConfigError(
                f"Device '{device_id}' has {len(errors)} configuration error(s):\n"
                + "\n".join(f"  [{i + 1}] {err}" for i, err in enumerate(errors))
            )

        return sensors

    @classmethod
    def get_sensor_class(cls, sensor_type: SensorType) -> Type[Sensor]:
        try:
            return cls._registry[sensor_type]
        except KeyError:
            raise SensorNotRegisteredError(
                f"Sensor type '{sensor_type}' is not registered."
            ) from None