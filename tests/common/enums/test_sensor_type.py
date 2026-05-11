# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Sensor Type Enum Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <11-Feb-2026>
# *****************************************************************************
import pytest
from src.common.enums.sensor_type import SensorType

@pytest.mark.parametrize("sensor_type", list(SensorType))
def test_sensor_type_str_returns_value_lowercase(sensor_type: SensorType):
    """
    Ensure that the __str__ method returns the lowercase value of the enum.
    
    Guards against accidental changes to the __str__ implementation or
    enum value assignments that could break YAML configuration keys
    which rely on lowercase messaging protocol names.
    """

    assert str(sensor_type) == sensor_type.value
    assert sensor_type.value.islower()

def test_sensor_type_enum_values_are_unique():
    """
    Ensure that all enum values are unique.
    
    Guards against accidental removal of the @unique decorator or
    the addition of duplicate values that could cause subtle bugs
    in sensor type handling logic.
    """

    values = [v.value for v in SensorType]
    assert len(values) == len(set(values))

def test_sensor_type_enum_can_be_used_as_dict_key():
    """
    Ensure that enum members are hashable and can be used as dictionary keys.
    
    Guards against accidental changes to the enum class that would
    make members unhashable or otherwise incompatible with dicts,
    which are often used to map sensor-specific configurations or handlers.
    """

    test_dict = {sensor_type: f"value_{sensor_type.value}" for sensor_type in SensorType}
    for sensor_type in SensorType:
        assert test_dict[sensor_type] == f"value_{sensor_type.value}"

def test_sensor_type_parse_is_case_insensitive():
    """
    Ensure that sensor type parsing is case-insensitive.

    Guards against inconsistent configuration inputs (e.g. ENV vars,
    YAML files, or CLI arguments) where values may appear in different
    casing formats such as "BME280", "bme280", or "Bme280".
    """

    assert SensorType.parse("BME280") is SensorType.BME280

def test_sensor_type_parse_handles_mixed_case():
    """
    Ensure that mixed-case sensor type values are correctly normalized.

    Prevents failures when configuration sources use non-standard casing
    conventions, ensuring consistent internal representation regardless
    of input formatting.
    """

    assert SensorType.parse("BmE280") is SensorType.BME280

def test_sensor_type_parse_strips_whitespace():
    """
    Ensure that surrounding whitespace is ignored during parsing.

    Protects against common issues in environment files or manual config
    entries where values may include accidental leading or trailing spaces.
    """

    assert SensorType.parse("  bme280  ") is SensorType.BME280

def test_sensor_type_parse_rejects_invalid_values():
    """
    Ensure that invalid sensor type strings raise a ValueError.

    Guards against unsupported or misspelled configuration values that
    could otherwise lead to undefined application behavior.
    """

    with pytest.raises(ValueError):
        SensorType.parse("custom-unknown-sensor")

def test_sensor_type_parse_rejects_non_string_input():
    """
    Ensure that non-string inputs are rejected with a TypeError.

    Prevents silent failures or confusing runtime errors when configuration
    sources provide unexpected types (e.g. None, integers, or objects).
    """

    with pytest.raises(TypeError):
        SensorType.parse(None)  # pyright: ignore[reportArgumentType]