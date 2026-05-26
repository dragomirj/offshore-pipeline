# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] Sensor Factory
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <13-Feb-2026>
# *****************************************************************************
from __future__ import annotations
from src.common.enums.sensor_type import SensorType
from src.config import SensorConfig
from src.sensors.base import Sensor
from src.sensors.registry import SENSOR_REGISTRY

class SensorNotRegisteredError(Exception):
    """Raised when a sensor type is not present in the registry."""

class SensorConfigError(Exception):
    """Raised when sensor configuration is invalid."""

class SensorFactory:
    _registry: dict[SensorType, type[Sensor]] = dict(SENSOR_REGISTRY)

    @classmethod
    def create(cls, device_id: str, config: SensorConfig) -> Sensor:
        sensor_type = SensorType.parse(config.sensor_type)
        try:
            sensor_class = cls._registry[sensor_type]
        except KeyError:
            raise SensorNotRegisteredError(
                f"Sensor type '{config.sensor_type}' is not registered. Known types: {', '.join(str(t) for t in cls._registry)}."
            ) from None

        missing = sensor_class.REQUIRED_PARAMS - config.params.keys()

        if missing:
            raise SensorConfigError(
                f"Sensor '{config.sensor_id}' of type '{config.sensor_type}' is missing required params: {', '.join(sorted(missing))}."
            )

        return sensor_class(
            device_id=device_id,
            sensor_id=config.sensor_id,
            warmup_seconds=config.warmup_seconds,
            alert_thresholds=config.alert_thresholds,
            **config.params,
        )

    @classmethod
    def get_sensor_class(cls, sensor_type: SensorType) -> type[Sensor]:
        try:
            return cls._registry[sensor_type]
        except KeyError:
            raise SensorNotRegisteredError(
                f"Sensor type '{sensor_type}' is not registered."
            ) from None