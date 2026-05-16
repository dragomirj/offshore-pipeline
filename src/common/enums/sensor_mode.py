# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Sensor Mode Enum
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <14-May-2026>
# *****************************************************************************
from enum import Enum

class SensorMode(Enum):
    POLLED    = "polled"
    INTERRUPT = "interrupt"
