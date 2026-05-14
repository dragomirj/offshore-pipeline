# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [UTILS] Sensor Utils
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <07-May-2026>
# *****************************************************************************
from src.common.enums.sensor_type import SensorType
from src.common.models.sensor_reading import SensorReading

def create_dummy_reading(value: float) -> SensorReading:
    return SensorReading(
        device_id="dummyDeviceId",
        sensor_id="dummySensorId",
        sensor_type=SensorType.BME280,
        channel="test_channel",
        value=value,
        unit="unit",
    )