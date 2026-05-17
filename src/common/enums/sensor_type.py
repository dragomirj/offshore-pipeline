# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Sensor Type Enum
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <11-Feb-2026>
# *****************************************************************************
from enum import unique
from typing import Self
from src.common.enums.base import ParsableEnum
from src.common.enums.sensor_mode import SensorMode

@unique
class SensorType(ParsableEnum):
    """
    Sensor types available in the pipeline, each with an associated SensorMode.

    Selection rationale: these sensors produce continuous numeric signals
    across overlapping physical domains (temperature, humidity, gas concentration)
    which enables correlation analysis, supervised prediction, and anomaly detection
    in downstream Spark and ksqlDB jobs.

    Adding a new sensor type requires changes in the following places:
      1. Add the enum member here with the correct SensorMode
      2. Add a hardware driver in /src/sensors/drivers/<type>.py
      3. Register driver in /src/sensors/registry.py
      4. Add simulation profiles in /src/simulation/profiles/<type>_profiles.py
      5. Register simulation profiles in /src/simulation/registry.py
    """

    _mode: SensorMode  # instance attribute, not an enum member; assigned in __new__

    def __new__(cls, value: str, mode: SensorMode) -> Self:
        obj = object.__new__(cls)
        obj._value_ = value
        obj._mode   = mode
        return obj

    ADXL345 = ("adxl345", SensorMode.INTERRUPT)
    BME280  = ("bme280",  SensorMode.POLLED)
    MQ7     = ("mq7",     SensorMode.POLLED)
    MQ135   = ("mq135",   SensorMode.POLLED)
    SCD40   = ("scd40",   SensorMode.POLLED)

    @property
    def mode(self) -> SensorMode:  # pragma: no cover
        return self._mode