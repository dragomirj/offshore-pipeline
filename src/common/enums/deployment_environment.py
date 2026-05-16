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
    SIMULATION  = "simulation"
    DEVELOPMENT = "development"
    STAGING     = "staging"
    PRODUCTION  = "production"

    _SUPPORTS_SIMULATION:               ClassVar[frozenset["DeploymentEnvironment"]]
    _REQUIRES_STRUCTURED_SERIALIZATION: ClassVar[frozenset["DeploymentEnvironment"]]
    _REQUIRES_ENCRYPTION:               ClassVar[frozenset["DeploymentEnvironment"]]

    def supports_simulation(self) -> bool:
        """True when simulated sensor data is permitted in this environment."""
        return self in self._SUPPORTS_SIMULATION
    
    def requires_structured_serialization(self) -> bool:
        """True when a non-JSON serialization format is required in this environment."""
        return self in self._REQUIRES_STRUCTURED_SERIALIZATION

    def requires_encryption(self) -> bool:
        """True when encryption is required in this environment."""
        return self in self._REQUIRES_ENCRYPTION
    
# Defined after the class so all members exist before the frozenset references them
DeploymentEnvironment._SUPPORTS_SIMULATION = frozenset({  # pyright: ignore[reportPrivateUsage]
    DeploymentEnvironment.SIMULATION,
    DeploymentEnvironment.DEVELOPMENT,
    DeploymentEnvironment.STAGING
})

DeploymentEnvironment._REQUIRES_STRUCTURED_SERIALIZATION = frozenset({  # pyright: ignore[reportPrivateUsage]
    DeploymentEnvironment.DEVELOPMENT,
    DeploymentEnvironment.STAGING,
    DeploymentEnvironment.PRODUCTION,
})

DeploymentEnvironment._REQUIRES_ENCRYPTION = frozenset({  # pyright: ignore[reportPrivateUsage]
    DeploymentEnvironment.STAGING,
    DeploymentEnvironment.PRODUCTION,
})