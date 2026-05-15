# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] Simulation Registry
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <30-Apr-2026>
# *****************************************************************************
from src.common.enums.sensor_type import SensorType
from src.common.models.channel_profile import ChannelProfile
from src.simulation.profiles.bme280_profiles import BME280_PROFILES
from src.simulation.profiles.mq135_profiles import MQ135_PROFILES
from src.simulation.profiles.mq7_profiles import MQ7_PROFILES
from src.simulation.profiles.scd40_profiles import SCD40_PROFILES

# Maps SensorType to concrete simulation profiles; defined once to avoid duplication
SIMULATION_REGISTRY: dict[SensorType, list[ChannelProfile]] = {
    SensorType.BME280:  BME280_PROFILES,
    SensorType.MQ135:   MQ135_PROFILES,
    SensorType.SCD40:   SCD40_PROFILES,
    SensorType.MQ7:     MQ7_PROFILES,
}
