# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [UTILS] Sensor Utils
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <07-May-2026>
# *****************************************************************************
from types import MappingProxyType
from src.common.enums.sensor_type import SensorType
from src.common.models.channel_profile import ChannelProfile
from src.common.models.sensor_reading import Metadata, SensorReading

def create_dummy_reading(
    value: float = 1.0, 
    metadata: Metadata = MappingProxyType({})
) -> SensorReading:
    return SensorReading(
        device_id="dummyDeviceId",
        sensor_id="dummySensorId",
        sensor_type=SensorType.BME280,
        channel="dummy_channel",
        value=value,
        unit="dummy_unit",
        metadata=metadata,
    )

def create_dummy_profile(
    mean: float = 1.0,
    std_dev: float = 0.4,
    alert_threshold: float | None = None,
) -> ChannelProfile:
    return ChannelProfile(
        channel="dummy_channel",
        unit="dummy_unit",
        sensor_type=SensorType.BME280,
        min_value=0.0,
        max_value=5.0,
        mean=mean,
        std_dev=std_dev,
        alert_threshold=alert_threshold,
    )
