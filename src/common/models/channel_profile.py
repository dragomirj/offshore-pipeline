# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Channel Profile Model
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <19-Feb-2026>
# ***************************************************************************** 
from __future__ import annotations
import math
from dataclasses import dataclass, field
from src.common.enums.sensor_type import SensorType

@dataclass
class ChannelProfile:
    channel:                    str
    unit:                       str
    sensor_type:                SensorType
    min_value:                  float
    max_value:                  float
    mean:                       float
    std_dev:                    float
    mean_reversion_speed:       float = 0.3
    volatility:                 float = 1.0
    spike_probability:          float = 0.02
    spike_magnitude_multiplier: float = 3.0
    spike_duration_ticks:       int   = 5
    alert_threshold:            float = field(default=float("nan"))

    def __post_init__(self) -> None:
        if math.isnan(self.alert_threshold):
            # Gaussian default. Set explicitly in the profile for non-Gaussian processes like Cox-Ingersoll-Ross (CIR).
            self.alert_threshold = self.mean + 2.5 * self.std_dev