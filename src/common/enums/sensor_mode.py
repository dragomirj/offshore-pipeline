# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Sensor Mode Enum
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <14-May-2026>
# *****************************************************************************
from enum import Enum, unique

@unique
class SensorMode(Enum):
    """
    Governs how a sensor delivers readings. Always inferred from SensorType and never
    parsed from config directly. See Readable.blocks_on_read for the behavioral
    contract each mode imposes on callers.
    """

    POLLED    = "polled"
    INTERRUPT = "interrupt"
