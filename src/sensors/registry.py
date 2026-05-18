# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] Sensor Registry
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <13-Feb-2026>
# *****************************************************************************
from src.sensors.base import Sensor
from src.common.enums.sensor_type import SensorType
from src.sensors.drivers.adxl345 import ADXL345Sensor
from src.sensors.drivers.bme280 import BME280Sensor
from src.sensors.drivers.mq7 import MQ7Sensor
from src.sensors.drivers.mq135 import MQ135Sensor
from src.sensors.drivers.scd40 import SCD40Sensor

# Maps SensorType to concrete sensor classes; defined once to avoid duplication
SENSOR_REGISTRY: dict[SensorType, type[Sensor]] = {
    SensorType.ADXL345: ADXL345Sensor,
    SensorType.BME280:  BME280Sensor,
    SensorType.MQ7:     MQ7Sensor,
    SensorType.MQ135:   MQ135Sensor,
    SensorType.SCD40:   SCD40Sensor,
}