# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] JSON Serializer Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <25-May-2026>
# *****************************************************************************
import json
import pytest
from src.common.enums.serialization_format import SerializationFormat
from src.common.models.sensor_event import SimulationInfo
from src.common.serialization.errors import MalformedPayloadError, MissingFieldError, SchemaViolationError
from src.common.serialization.serializers.json.json_serializer import JsonSerializer
from tests.utils.events import create_dummy_event

_serializer = JsonSerializer()

def test_format_is_json():
    assert _serializer.format == SerializationFormat.JSON

def test_roundtrip_without_simulation():
    event = create_dummy_event()
    assert _serializer.deserialize(_serializer.serialize(event)) == event

def test_roundtrip_with_simulation():
    event = create_dummy_event(simulation=SimulationInfo(simulation_type="ornstein_uhlenbeck"))
    assert _serializer.deserialize(_serializer.serialize(event)) == event

def test_deserialize_raises_on_invalid_json():
    with pytest.raises(MalformedPayloadError):
        _serializer.deserialize(b"not json")

def test_deserialize_raises_on_missing_field():
    raw = json.loads(_serializer.serialize(create_dummy_event()))
    del raw["occurred_at"]
    with pytest.raises(MissingFieldError):
        _serializer.deserialize(json.dumps(raw).encode())

def test_deserialize_raises_on_type_violation():
    raw = json.loads(_serializer.serialize(create_dummy_event()))
    raw["occurred_at"] = "not_a_number"
    with pytest.raises(SchemaViolationError):
        _serializer.deserialize(json.dumps(raw).encode())
