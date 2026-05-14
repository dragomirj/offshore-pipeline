# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Deployment Environment Enum
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <11-Feb-2026>
# ***************************************************************************** 
from enum import unique
from src.common.enums.base import ParsableEnum

@unique
class DeploymentEnvironment(ParsableEnum):
    """
    Enum of deployment environments for an event-driven, IoT-focused ETL system.
    Values are normalized to lowercase to ensure consistent identifiers across the codebase and configuration (e.g., YAML keys).
    """

    SIMULATION  = "simulation"
    DEVELOPMENT = "development"
    STAGING     = "staging"
    PRODUCTION  = "production"