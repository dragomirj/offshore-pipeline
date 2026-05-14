# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Deployment Environment Enum
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <11-Feb-2026>
# ***************************************************************************** 
from enum import unique
from typing import ClassVar
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

    _SUPPORTS_SIMULATION: ClassVar[frozenset["DeploymentEnvironment"]]

    def supports_simulation(self) -> bool:
        """True when simulated sensor data is permitted in this environment."""
        return self in self._SUPPORTS_SIMULATION
    
# Defined after the class so all members exist before the frozenset references them
DeploymentEnvironment._SUPPORTS_SIMULATION = frozenset({  # pyright: ignore[reportPrivateUsage]
    DeploymentEnvironment.SIMULATION,
    DeploymentEnvironment.DEVELOPMENT,
    DeploymentEnvironment.STAGING
})