# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] ADXL345 Sensor Profiles
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <13-May-2026>
# *****************************************************************************
from src.common.models.channel_profile import ChannelProfile
from src.common.enums.sensor_type import SensorType

ADXL345_PROFILES = [
    ChannelProfile(
        channel="vibration_g",
        unit="g",
        sensor_type=SensorType.ADXL345,
        min_value=0.0,
        max_value=5.0,
        mean=0.25,
        std_dev=0.1,
        mean_reversion_speed=0.15,
        volatility=0.11,
        spike_probability=0.01,
        spike_magnitude_multiplier=5.0,
        spike_duration_ticks=8,
        alert_threshold=0.50,
    ),
]
