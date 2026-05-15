# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] MQ135 Sensor Profiles
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <28-Apr-2026>
# ***************************************************************************** 
from src.common.models.channel_profile import ChannelProfile
from src.common.enums.sensor_type import SensorType

MQ135_PROFILES = [
    ChannelProfile(
        channel="co2_ppm",
        unit="ppm",
        sensor_type=SensorType.MQ135,
        min_value=300.0,
        max_value=5000.0,
        mean=950.0,
        std_dev=80.0,
        mean_reversion_speed=0.12,
        volatility=18.0,
        spike_probability=0.015,
        spike_magnitude_multiplier=3.5,
        spike_duration_ticks=10,
    ),
    ChannelProfile(
        channel="nh3_ppm",
        unit="ppm",
        sensor_type=SensorType.MQ135,
        min_value=1.0,
        max_value=300.0,
        mean=8.0,
        std_dev=3.0,
        mean_reversion_speed=0.15,
        volatility=1.5,
        spike_probability=0.010,
        spike_magnitude_multiplier=4.0,
        spike_duration_ticks=14,
    ),
]