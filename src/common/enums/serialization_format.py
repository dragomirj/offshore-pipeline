# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Serialization Format Enum
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <04-May-2026>
# *****************************************************************************
from enum import unique
from src.common.enums.base import ParsableEnum

@unique
class SerializationFormat(ParsableEnum):
    """
    Serialization formats for sensor events.

    - JSON: Permitted in SIMULATION only. Prohibited in DEVELOPMENT, STAGING, and PRODUCTION.
      See: DeploymentEnvironment.requires_structured_serialization()

    - PROTOBUF: Permitted in all environments.
    """

    JSON     = "json"
    PROTOBUF = "protobuf"
