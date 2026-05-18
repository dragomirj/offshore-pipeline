# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Messaging Protocol Enum
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <11-Feb-2026>
# *****************************************************************************
from enum import unique
from src.common.enums.base import ParsableEnum

@unique
class MessagingProtocol(ParsableEnum):
    """
    Transport protocols used across the platform.

    - MQTT: used by IoT devices to publish sensor readings to a broker.
    - KAFKA: broker to downstream consumers (Spark, ksqlDB). Planned.
    """

    MQTT = "mqtt"