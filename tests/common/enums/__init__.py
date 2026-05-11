# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Deployment Environment Enum Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <11-Feb-2026>
# *****************************************************************************
import pytest
from src.common.enums.deployment_environment import DeploymentEnvironment

@pytest.mark.parametrize("deployment_environment", list(DeploymentEnvironment))
def test_deployment_environment_str_returns_value_lowercase(deployment_environment: DeploymentEnvironment):
    """
    Ensure that the __str__ method returns the lowercase value of the enum.
    
    Guards against accidental changes to the __str__ implementation or
    enum value assignments that could break YAML configuration keys
    which rely on lowercase deployment environment names.
    """

    assert str(deployment_environment) == deployment_environment.value
    assert deployment_environment.value.islower()

def test_deployment_environment_enum_values_are_unique():
    """
    Ensure that all enum values are unique.
    
    Guards against accidental removal of the @unique decorator or
    the addition of duplicate values that could cause subtle bugs
    in deployment environment handling logic.
    """

    values = [v.value for v in DeploymentEnvironment]
    assert len(values) == len(set(values))

def test_deployment_environment_enum_can_be_used_as_dict_key():
    """
    Ensure that enum members are hashable and can be used as dictionary keys.
    
    Guards against accidental changes to the enum class that would
    make members unhashable or otherwise incompatible with dicts,
    which are often used to map environment-specific configurations or handlers.
    """

    test_dict = {environment: f"value_{environment.value}" for environment in DeploymentEnvironment}
    for environment in DeploymentEnvironment:
        assert test_dict[environment] == f"value_{environment.value}"

def test_deployment_environment_parse_is_case_insensitive():
    """
    Ensure that deployment environment parsing is case-insensitive.

    Guards against inconsistent configuration inputs (e.g. ENV vars,
    YAML files, or CLI arguments) where values may appear in different
    casing formats such as "PRODUCTION", "production", or "Production".
    """

    assert DeploymentEnvironment.parse("PRODUCTION") is DeploymentEnvironment.PRODUCTION

def test_deployment_environment_parse_handles_mixed_case():
    """
    Ensure that mixed-case deployment environment values are correctly normalized.

    Prevents failures when configuration sources use non-standard casing
    conventions, ensuring consistent internal representation regardless
    of input formatting.
    """

    assert DeploymentEnvironment.parse("PrOdUcTiOn") is DeploymentEnvironment.PRODUCTION

def test_deployment_environment_parse_strips_whitespace():
    """
    Ensure that surrounding whitespace is ignored during parsing.

    Protects against common issues in environment files or manual config
    entries where values may include accidental leading or trailing spaces.
    """

    assert DeploymentEnvironment.parse("  staging  ") is DeploymentEnvironment.STAGING

def test_deployment_environment_parse_rejects_invalid_values():
    """
    Ensure that invalid deployment environment strings raise a ValueError.

    Guards against unsupported or misspelled configuration values that
    could otherwise lead to undefined application behavior.
    """

    with pytest.raises(ValueError):
        DeploymentEnvironment.parse("custom-unknown-environment")

def test_deployment_environment_parse_rejects_non_string_input():
    """
    Ensure that non-string inputs are rejected with a TypeError.

    Prevents silent failures or confusing runtime errors when configuration
    sources provide unexpected types (e.g. None, integers, or objects).
    """

    with pytest.raises(TypeError):
        DeploymentEnvironment.parse(None)  # pyright: ignore[reportArgumentType]