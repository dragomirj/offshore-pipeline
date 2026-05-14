# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Sensor Reading Model
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <12-Feb-2026>
# ***************************************************************************** 
from typing import TypeAlias
from dataclasses import dataclass, field
from datetime import datetime, timezone
from src.common.enums.sensor_type import SensorType

MetadataValue: TypeAlias = str | int | float | bool | None
Metadata:      TypeAlias = dict[str, MetadataValue]

@dataclass(frozen=True, slots=True)
class SensorReading:
    device_id:   str
    sensor_id:   str
    sensor_type: SensorType
    channel:     str
    value:       float
    unit:        str
    timestamp:   datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata:    Metadata = field(default_factory=lambda: {})