# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Sensor Type Enum
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <11-Feb-2026>
# *****************************************************************************
from enum import unique
from src.common.enums.base import ParsableEnum

@unique
class SensorType(ParsableEnum):
    """
    Enum of sensor types for an event-driven, IoT-focused ETL system.
    Values are normalized to lowercase to ensure consistent identifiers across the codebase and configuration (e.g., YAML keys).

    Selection rationale: these sensors produce continuous numeric signals
    across overlapping physical domains (temperature, humidity, gas concentration)
    which enables correlation analysis, supervised prediction, and anomaly detection
    in downstream Spark and ksqlDB jobs.
    """

    BME280 = "bme280"
    MQ7    = "mq7"
    MQ135  = "mq135"
    SCD40  = "scd40"