# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Device Mode Enum
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <19-May-2026>
# *****************************************************************************
from enum import unique
from src.common.enums.base import ParsableEnum

@unique
class DeviceMode(ParsableEnum):
    SIMULATION = "simulation"
    HARDWARE   = "hardware"
