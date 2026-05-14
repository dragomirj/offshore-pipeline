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
    Enum of messaging protocols for an event-driven, IoT-focused ETL system.
    Values are normalized to lowercase to ensure consistent identifiers across the codebase and configuration (e.g., YAML keys).
    """

    MQTT = 'mqtt'