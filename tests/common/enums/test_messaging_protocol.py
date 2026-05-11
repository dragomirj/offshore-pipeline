# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Messaging Protocol Enum Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <11-Feb-2026>
# *****************************************************************************
import pytest
from src.common.enums.messaging_protocol import MessagingProtocol

@pytest.mark.parametrize("messaging_protocol", list(MessagingProtocol))
def test_messaging_protocol_str_returns_value_lowercase(messaging_protocol: MessagingProtocol):
    """
    Ensure that the __str__ method returns the lowercase value of the enum.
    
    Guards against accidental changes to the __str__ implementation or
    enum value assignments that could break YAML configuration keys
    which rely on lowercase messaging protocol names.
    """

    assert str(messaging_protocol) == messaging_protocol.value
    assert messaging_protocol.value.islower()

def test_messaging_protocol_enum_values_are_unique():
    """
    Ensure that all enum values are unique.
    
    Guards against accidental removal of the @unique decorator or
    the addition of duplicate values that could cause subtle bugs
    in messaging protocol handling logic.
    """

    values = [v.value for v in MessagingProtocol]
    assert len(values) == len(set(values))

def test_messaging_protocol_enum_can_be_used_as_dict_key():
    """
    Ensure that enum members are hashable and can be used as dictionary keys.
    
    Guards against accidental changes to the enum class that would
    make members unhashable or otherwise incompatible with dicts,
    which are often used to map protocol-specific configurations or handlers.
    """

    test_dict = {protocol: f"value_{protocol.value}" for protocol in MessagingProtocol}
    for protocol in MessagingProtocol:
        assert test_dict[protocol] == f"value_{protocol.value}"

def test_messaging_protocol_parse_is_case_insensitive():
    """
    Ensure that messaging protocol parsing is case-insensitive.

    Guards against inconsistent configuration inputs (e.g. ENV vars,
    YAML files, or CLI arguments) where values may appear in different
    casing formats such as "MQTT", "mqtt", or "Mqtt".
    """

    assert MessagingProtocol.parse("MQTT") is MessagingProtocol.MQTT

def test_messaging_protocol_parse_handles_mixed_case():
    """
    Ensure that mixed-case messaging protocol values are correctly normalized.

    Prevents failures when configuration sources use non-standard casing
    conventions, ensuring consistent internal representation regardless
    of input formatting.
    """

    assert MessagingProtocol.parse("MqTt") is MessagingProtocol.MQTT

def test_messaging_protocol_parse_strips_whitespace():
    """
    Ensure that surrounding whitespace is ignored during parsing.

    Protects against common issues in environment files or manual config
    entries where values may include accidental leading or trailing spaces.
    """

    assert MessagingProtocol.parse("  mqtt  ") is MessagingProtocol.MQTT

def test_messaging_protocol_parse_rejects_invalid_values():
    """
    Ensure that invalid messaging protocol strings raise a ValueError.

    Guards against unsupported or misspelled configuration values that
    could otherwise lead to undefined application behavior.
    """

    with pytest.raises(ValueError):
        MessagingProtocol.parse("custom-unknown-protocol")

def test_messaging_protocol_parse_rejects_non_string_input():
    """
    Ensure that non-string inputs are rejected with a TypeError.

    Prevents silent failures or confusing runtime errors when configuration
    sources provide unexpected types (e.g. None, integers, or objects).
    """

    with pytest.raises(TypeError):
        MessagingProtocol.parse(None)  # pyright: ignore[reportArgumentType]