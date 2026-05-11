# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Deployment Environment Enum
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <11-Feb-2026>
# ***************************************************************************** 
from enum import Enum, unique

@unique
class DeploymentEnvironment(Enum):
    """
    Enum of deployment environments for an event-driven, IoT-focused ETL system.
    Values are normalized to lowercase to ensure consistent identifiers across the codebase and configuration (e.g., YAML keys).
    """

    SIMULATION  = "simulation"
    DEVELOPMENT = "development"
    STAGING     = "staging"
    PRODUCTION  = "production"
    
    @classmethod
    def parse(cls, value: str) -> "DeploymentEnvironment":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"Expected string, got {type(value).__name__}")
        return cls(value.strip().lower())

    def __str__(self) -> str:
        """Return the lowercase value of the enum member."""
        return self.value