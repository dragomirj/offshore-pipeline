# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Deployment Environment Enum
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <04-May-2026>
# ***************************************************************************** 
import pytest
from src.common.enums.deployment_environment import DeploymentEnvironment

@pytest.mark.parametrize(
    "env,expected",
    [
        (DeploymentEnvironment.SIMULATION,  True),
        (DeploymentEnvironment.DEVELOPMENT, True),
        (DeploymentEnvironment.STAGING,     True),
        (DeploymentEnvironment.PRODUCTION,  False),
    ],
)
def test_supports_simulation(env: DeploymentEnvironment, expected: bool):
    assert env.supports_simulation() is expected


@pytest.mark.parametrize(
    "env,expected",
    [
        (DeploymentEnvironment.SIMULATION,  False),
        (DeploymentEnvironment.DEVELOPMENT, True),
        (DeploymentEnvironment.STAGING,     True),
        (DeploymentEnvironment.PRODUCTION,  True),
    ],
)
def test_requires_structured_serialization(env: DeploymentEnvironment, expected: bool):
    assert env.requires_structured_serialization() is expected


@pytest.mark.parametrize(
    "env,expected",
    [
        (DeploymentEnvironment.SIMULATION,  False),
        (DeploymentEnvironment.DEVELOPMENT, False),
        (DeploymentEnvironment.STAGING,     True),
        (DeploymentEnvironment.PRODUCTION,  True),
    ],
)
def test_requires_encryption(env: DeploymentEnvironment, expected: bool):
    assert env.requires_encryption() is expected