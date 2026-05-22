# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [EVENTS] Event Assembler Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <21-May-2026>
# *****************************************************************************
import pytest
from datetime import datetime, timezone
from types import MappingProxyType
from unittest.mock import patch
from src.common.enums.sensor_type import SensorType
from src.common.models.sensor_event import ChannelMetadata, Location, SensorEvent
from src.common.models.sensor_reading import SensorReading
from src.events.assembler import AssemblerConfig, EventAssembler

DUMMY_DEVICE_ID = "dummyDeviceId"
DUMMY_SENSOR_ID = "dummySensorId"
DUMMY_FIRMWARE_VERSION = "dummyFirmwareVersion"
DUMMY_LOCATION = Location(lat=0.0, lon=0.0)
DUMMY_TAGS = ("dummy_tag1", "dummy_tag2", "dummy_tag3")
DUMMY_CONFIG = AssemblerConfig(firmware_version=DUMMY_FIRMWARE_VERSION, location=DUMMY_LOCATION, tags=DUMMY_TAGS)
DUMMY_CHANNEL_A = "dummy_channel_a"
DUMMY_CHANNEL_B = "dummy_channel_b"
DUMMY_VALUE  = 22.1
SIM_TYPE_OU  = "ornstein_uhlenbeck"
SIM_TYPE_CIR = "cox_ingersoll_ross"

def _make_reading(
    channel: str = DUMMY_CHANNEL_A,
    value: float = 21.5,
    device_id: str = DUMMY_DEVICE_ID,
    sensor_id: str = DUMMY_SENSOR_ID,
    alert_threshold: float = 80.0,
    spiking: bool | None = None,
    simulation_type: str | None = None,
    timestamp: datetime | None = None
) -> SensorReading:
    metadata: dict = {"alert_threshold": alert_threshold}  # pyright: ignore[reportUnknownVariableType, reportMissingTypeArgument]
    if spiking is not None:
        metadata["spiking"] = spiking
    if simulation_type is not None:
        metadata["simulation_type"] = simulation_type
    kwargs = {} if timestamp is None else {"timestamp": timestamp}
    
    return SensorReading(
        device_id=device_id,
        sensor_id=sensor_id,
        sensor_type=SensorType.BME280,
        channel=channel,
        value=value,
        unit="dummy_unit",
        metadata=metadata,  # pyright: ignore[reportUnknownArgumentType]
        **kwargs,
    )

def _make_assembler(config: AssemblerConfig = DUMMY_CONFIG) -> EventAssembler:
    return EventAssembler(config)

def test_assemble_raises_on_empty_readings():
    with pytest.raises(ValueError, match="empty"):
        _make_assembler().assemble([])

def test_assemble_returns_sensor_event():
    result = _make_assembler().assemble([_make_reading()])
    assert isinstance(result, SensorEvent)

def test_assemble_occurred_at_is_earliest_timestamp_in_millis():
    t1 = datetime(2026, 5, 21, 10, 0, 0, tzinfo=timezone.utc)
    t2  = datetime(2026, 5, 21, 10, 0, 5, tzinfo=timezone.utc)
    readings = [
        _make_reading(channel=DUMMY_CHANNEL_A, timestamp=t2),
        _make_reading(channel=DUMMY_CHANNEL_B, timestamp=t1),
    ]

    expected = int(t1.timestamp() * 1000)
    assert _make_assembler().assemble(readings).occurred_at == expected

def test_assemble_occurred_at_single_reading_matches_its_timestamp():
    t = datetime(2026, 5, 21, 12, 0, 0, tzinfo=timezone.utc)
    expected = int(t.timestamp() * 1000)
    assert _make_assembler().assemble([_make_reading(timestamp=t)]).occurred_at == expected

def test_assemble_ingested_at_is_current_time_in_millis():
    fixed_ns = 1_716_379_200_000_000_000
    with patch("src.events.assembler.time") as mock_time:
        mock_time.time_ns.return_value = fixed_ns
        result = _make_assembler().assemble([_make_reading()])
    assert result.ingested_at == fixed_ns // 1_000_000

def test_assemble_device_id_matches_first_reading():
    result = _make_assembler().assemble([_make_reading(device_id=DUMMY_DEVICE_ID)])
    assert result.device.device_id == DUMMY_DEVICE_ID

def test_assemble_sensor_id_matches_first_reading():
    result = _make_assembler().assemble([_make_reading(sensor_id=DUMMY_SENSOR_ID)])
    assert result.device.sensor_id == DUMMY_SENSOR_ID

def test_assemble_firmware_version_comes_from_config():
    result = _make_assembler().assemble([_make_reading()])
    assert result.device.firmware_version == DUMMY_FIRMWARE_VERSION

def test_assemble_location_comes_from_config():
    result = _make_assembler().assemble([_make_reading()])
    assert result.device.location == DUMMY_LOCATION

def test_assemble_data_maps_channel_to_value():
    result = _make_assembler().assemble([_make_reading(channel=DUMMY_CHANNEL_A, value=DUMMY_VALUE)])
    assert result.data[DUMMY_CHANNEL_A] == DUMMY_VALUE

def test_assemble_data_contains_all_channels():
    readings = [
        _make_reading(channel=DUMMY_CHANNEL_A, value=DUMMY_VALUE),
        _make_reading(channel=DUMMY_CHANNEL_B, value=55.0),
    ]

    result = _make_assembler().assemble(readings)
    assert set(result.data.keys()) == {DUMMY_CHANNEL_A, DUMMY_CHANNEL_B}

def test_assemble_data_is_immutable():
    result = _make_assembler().assemble([_make_reading()])
    assert isinstance(result.data, MappingProxyType)

def test_assemble_channels_contains_all_channels():
    readings = [
        _make_reading(channel=DUMMY_CHANNEL_A),
        _make_reading(channel=DUMMY_CHANNEL_B),
    ]

    result = _make_assembler().assemble(readings)
    assert set(result.channels.keys()) == {DUMMY_CHANNEL_A, DUMMY_CHANNEL_B}

def test_assemble_channels_is_immutable():
    result = _make_assembler().assemble([_make_reading()])
    assert isinstance(result.channels, MappingProxyType)

def test_assemble_alert_threshold_is_set_on_channel():
    result = _make_assembler().assemble([_make_reading(channel=DUMMY_CHANNEL_A, alert_threshold=95.0)])
    assert result.channels[DUMMY_CHANNEL_A].alert_threshold == 95.0

def test_assemble_spiking_defaults_to_false_when_absent_from_metadata():
    result = _make_assembler().assemble([_make_reading()])
    assert result.channels[DUMMY_CHANNEL_A].spiking is False

def test_assemble_spiking_is_true_when_set_in_metadata():
    result = _make_assembler().assemble([_make_reading(spiking=True)])
    assert result.channels[DUMMY_CHANNEL_A].spiking is True

def test_assemble_spiking_is_false_when_explicitly_false_in_metadata():
    result = _make_assembler().assemble([_make_reading(spiking=False)])
    assert result.channels[DUMMY_CHANNEL_A].spiking is False

def test_assemble_channel_metadata_type():
    result = _make_assembler().assemble([_make_reading()])
    assert isinstance(result.channels[DUMMY_CHANNEL_A], ChannelMetadata)

def test_assemble_tags_match_config():
    result = _make_assembler().assemble([_make_reading()])
    assert result.tags == DUMMY_TAGS

def test_assemble_tags_empty_when_config_has_no_tags():
    config = AssemblerConfig(firmware_version=DUMMY_FIRMWARE_VERSION, location=DUMMY_LOCATION, tags=())
    result = EventAssembler(config).assemble([_make_reading()])
    assert result.tags == ()

def test_assemble_simulation_is_none_when_no_simulation_type_in_metadata():
    result = _make_assembler().assemble([_make_reading()])
    assert result.simulation is None

def test_assemble_simulation_is_set_when_simulation_type_present():
    result = _make_assembler().assemble([_make_reading(simulation_type=SIM_TYPE_OU)])
    assert result.simulation is not None

def test_assemble_simulation_type_string_matches_metadata():
    result = _make_assembler().assemble([_make_reading(simulation_type=SIM_TYPE_OU)])
    assert result.simulation is not None
    assert result.simulation.simulation_type == SIM_TYPE_OU

def test_assemble_simulation_uses_first_reading_with_simulation_type():
    readings = [
        _make_reading(channel=DUMMY_CHANNEL_A, simulation_type=SIM_TYPE_OU),
        _make_reading(channel=DUMMY_CHANNEL_B, simulation_type=SIM_TYPE_CIR),
    ]

    result = _make_assembler().assemble(readings)
    assert result.simulation is not None
    assert result.simulation.simulation_type == SIM_TYPE_OU

def test_assemble_simulation_is_none_when_only_some_readings_lack_simulation_type():
    readings = [
        _make_reading(channel=DUMMY_CHANNEL_A),
        _make_reading(channel=DUMMY_CHANNEL_B),
    ]
    
    result = _make_assembler().assemble(readings)
    assert result.simulation is None
