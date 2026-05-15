# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] MQ7 Sensor Profiles
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <28-Apr-2026>
# ***************************************************************************** 
from src.common.models.channel_profile import ChannelProfile
from src.common.enums.sensor_type import SensorType

MQ7_PROFILES = [
    ChannelProfile(
        channel="co_ppm",
        unit="ppm",
        sensor_type=SensorType.MQ7,
        min_value=5.0,
        max_value=2000.0,
        mean=15.0,
        std_dev=5.0,
        mean_reversion_speed=0.2,
        volatility=2.0,
        spike_probability=0.012,
        spike_magnitude_multiplier=6.0,
        spike_duration_ticks=10,
    ),
]