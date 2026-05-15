# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] SCD40 Sensor Profiles
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <28-Apr-2026>
# ***************************************************************************** 
from src.common.models.channel_profile import ChannelProfile
from src.common.enums.sensor_type import SensorType

SCD40_PROFILES = [
    ChannelProfile(
        channel="co2_ppm",
        unit="ppm",
        sensor_type=SensorType.SCD40,
        min_value=400.0,
        max_value=5000.0,
        mean=800.0,
        std_dev=60.0,
        mean_reversion_speed=0.1,
        volatility=12.0,
        spike_probability=0.010,
        spike_magnitude_multiplier=3.5,
        spike_duration_ticks=12,
    ),
    ChannelProfile(
        channel="temperature_c",
        unit="celsius",
        sensor_type=SensorType.SCD40,
        min_value=-10.0,
        max_value=60.0,
        mean=24.0,
        std_dev=1.5,
        mean_reversion_speed=0.05,
        volatility=0.3,
        spike_probability=0.004,
        spike_magnitude_multiplier=3.0,
        spike_duration_ticks=20,
    ),
    ChannelProfile(
        channel="humidity_rh",
        unit="rh_percent",
        sensor_type=SensorType.SCD40,
        min_value=0.0,
        max_value=100.0,
        mean=46.0,
        std_dev=5.0,
        mean_reversion_speed=0.08,
        volatility=1.0,
        spike_probability=0.005,
        spike_magnitude_multiplier=2.5,
        spike_duration_ticks=15,
    ),
]