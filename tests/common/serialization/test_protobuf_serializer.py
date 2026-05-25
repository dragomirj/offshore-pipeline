# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Protobuf Serializer Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <25-May-2026>
# *****************************************************************************
import pytest
from src.common.enums.serialization_format import SerializationFormat
from src.common.models.sensor_event import SimulationInfo
from src.common.serialization.errors import MalformedPayloadError
from src.common.serialization.serializers.protobuf.protobuf_serializer import ProtobufSerializer
from tests.utils.events import create_dummy_event

_serializer = ProtobufSerializer()

def test_format_is_protobuf():
    assert _serializer.format == SerializationFormat.PROTOBUF

def test_roundtrip_without_simulation():
    event = create_dummy_event()
    assert _serializer.deserialize(_serializer.serialize(event)) == event

def test_roundtrip_with_simulation():
    event = create_dummy_event(simulation=SimulationInfo(simulation_type="ornstein_uhlenbeck"))
    assert _serializer.deserialize(_serializer.serialize(event)) == event

def test_deserialize_raises_on_garbage_bytes():
    with pytest.raises(MalformedPayloadError):
        _serializer.deserialize(b"\x00\xFF\xAB")
