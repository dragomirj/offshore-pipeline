# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] BME280 Sensor Profiles
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <28-Apr-2026>
# ***************************************************************************** 
from src.common.models.channel_profile import ChannelProfile
from src.common.enums.sensor_type import SensorType

BME280_PROFILES = [
    ChannelProfile(
        channel="temperature_c",
        unit="celsius",
        sensor_type=SensorType.BME280,
        min_value=-10.0,
        max_value=60.0,
        mean=22.0,
        std_dev=1.5,
        mean_reversion_speed=0.05,
        volatility=0.3,
        spike_probability=0.005,
        spike_magnitude_multiplier=3.0,
        spike_duration_ticks=20,
    ),
    ChannelProfile(
        channel="humidity_rh",
        unit="rh_percent",
        sensor_type=SensorType.BME280,
        min_value=10.0,
        max_value=95.0,
        mean=50.0,
        std_dev=5.0,
        mean_reversion_speed=0.08,
        volatility=1.0,
        spike_probability=0.005,
        spike_magnitude_multiplier=2.5,
        spike_duration_ticks=15,
    ),
    ChannelProfile(
        channel="pressure_hpa",
        unit="hpa",
        sensor_type=SensorType.BME280,
        min_value=870.0,
        max_value=1084.0,
        mean=1013.0,
        std_dev=4.0,
        mean_reversion_speed=0.03,
        volatility=0.5,
        spike_probability=0.003,
        spike_magnitude_multiplier=2.0,
        spike_duration_ticks=8,
    ),
]