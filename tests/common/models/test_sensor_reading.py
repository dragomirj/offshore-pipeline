# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Sensor Reading Model Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <18-May-2026>
# *****************************************************************************
import pytest
from types import MappingProxyType
from tests.utils.sensors import create_dummy_reading

def test_metadata_default_is_immutable():
    assert isinstance(create_dummy_reading().metadata, MappingProxyType)

def test_metadata_default_is_empty():
    assert len(create_dummy_reading().metadata) == 0

def test_metadata_wraps_plain_dict():
    assert isinstance(create_dummy_reading(metadata={"k": "v"}).metadata, MappingProxyType)

def test_metadata_preserves_values_from_plain_dict():
    assert create_dummy_reading(metadata={"k": "v"}).metadata["k"] == "v"

def test_metadata_wraps_mapping_proxy_type():
    assert isinstance(create_dummy_reading(metadata=MappingProxyType({"k": "v"})).metadata, MappingProxyType)

def test_metadata_mutation_raises():
    reading = create_dummy_reading(metadata={"k": "v"})
    with pytest.raises(TypeError):
        reading.metadata["k"] = "mutated"  # pyright: ignore[reportIndexIssue]
