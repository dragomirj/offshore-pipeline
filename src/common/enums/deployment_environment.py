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
    SIMULATION  = "simulation"
    DEVELOPMENT = "development"
    STAGING     = "staging"
    PRODUCTION  = "production"

    def supports_simulation(self) -> bool:
        """True when simulated sensor data is permitted in this environment."""
        return self in _SUPPORTS_SIMULATION

    def requires_structured_serialization(self) -> bool:
        """True when a non-JSON serialization format is required in this environment."""
        return self in _REQUIRES_STRUCTURED_SERIALIZATION

    def requires_encryption(self) -> bool:
        """True when encryption is required in this environment."""
        return self in _REQUIRES_ENCRYPTION

_SUPPORTS_SIMULATION = frozenset({
    DeploymentEnvironment.SIMULATION,
    DeploymentEnvironment.DEVELOPMENT,
    DeploymentEnvironment.STAGING,
})

_REQUIRES_STRUCTURED_SERIALIZATION = frozenset({
    DeploymentEnvironment.DEVELOPMENT,
    DeploymentEnvironment.STAGING,
    DeploymentEnvironment.PRODUCTION,
})

_REQUIRES_ENCRYPTION = frozenset({
    DeploymentEnvironment.STAGING,
    DeploymentEnvironment.PRODUCTION,
})