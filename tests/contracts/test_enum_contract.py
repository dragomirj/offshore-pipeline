# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [CONTRACTS] Enum Contract Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <27-Apr-2026>
# *****************************************************************************
import pytest
from enum import Enum
from tests.utils.enums import get_all_parsable_enums

ENUMS = get_all_parsable_enums("src.common.enums")

def get_parse(enum_cls: type[Enum]):
    return getattr(enum_cls, "parse")

@pytest.mark.parametrize("enum_cls", ENUMS)
def test_enum_str_returns_lowercase_value(enum_cls: type[Enum]):
    for member in enum_cls:
        assert str(member) == member.value
        assert member.value.islower()

@pytest.mark.parametrize("enum_cls", ENUMS)
def test_enum_parse_is_case_insensitive(enum_cls: type[Enum]):
    parse_fn = get_parse(enum_cls)

    for member in enum_cls:
        assert parse_fn(member.value.upper()) is member
        assert parse_fn(member.value.lower()) is member
        assert parse_fn(member.value.capitalize()) is member

@pytest.mark.parametrize("enum_cls", ENUMS)
def test_enum_parse_strips_whitespace(enum_cls: type[Enum]):
    parse_fn = get_parse(enum_cls)

    for member in enum_cls:
        assert parse_fn(f"  {member.value}  ") is member

@pytest.mark.parametrize("enum_cls", ENUMS)
def test_enum_parse_rejects_invalid_values(enum_cls: type[Enum]):
    parse_fn = get_parse(enum_cls)

    with pytest.raises(ValueError):
        parse_fn("invalid-value")

@pytest.mark.parametrize("enum_cls", ENUMS)
@pytest.mark.parametrize("value", [None, 7, object()])
def test_enum_parse_rejects_non_string_input(enum_cls: type[Enum], value: object):
    parse_fn = get_parse(enum_cls)

    with pytest.raises(TypeError):
        parse_fn(value)