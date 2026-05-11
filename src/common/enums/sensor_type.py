# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Sensor Type Enum
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <11-Feb-2026>
# *****************************************************************************
from enum import Enum, unique

@unique
class SensorType(Enum):
    """
    Enum of sensor types for an event-driven, IoT-focused ETL system.
    Values are normalized to lowercase to ensure consistent identifiers across the codebase and configuration (e.g., YAML keys).

    Selection rationale: these four sensors produce continuous numeric signals
    across overlapping physical domains (temperature, humidity, gas concentration)
    which enables correlation analysis, supervised prediction, and anomaly detection
    in downstream Spark and ksqlDB jobs.
    """

    BME280 = "bme280"
    MQ7    = "mq7"
    MQ135  = "mq135"
    SCD40  = "scd40"

    @classmethod
    def parse(cls, value: str) -> "SensorType":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"Expected string, got {type(value).__name__}")
        return cls(value.strip().lower())

    def __str__(self) -> str:
        """Return the lowercase value of the enum member."""
        return self.value