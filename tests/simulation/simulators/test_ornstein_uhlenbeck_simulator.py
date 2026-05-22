# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] OU Simulator Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <11-May-2026>
# *****************************************************************************
import pytest
from src.common.enums.sensor_type import SensorType
from src.common.models.channel_profile import ChannelProfile
from src.simulation.simulators.ornstein_uhlenbeck_simulator import OrnsteinUhlenbeckSimulator

DUMMY_DEVICE_ID = "dummyDeviceId"
DUMMY_SENSOR_ID = "dummySensorId"
PROFILE_MIN  = 0.0
PROFILE_MAX  = 100.0
PROFILE_MEAN = 50.0
PROFILE_STD  = 1.5
# Ornstein-Uhlenbeck (OU) has a Gaussian stationary distribution so the `mean + 2.5 * std_dev` default applies
EXPECTED_ALERT_THRESHOLD = PROFILE_MEAN + 2.5 * PROFILE_STD

def _make_simulator(n_profiles: int = 1) -> OrnsteinUhlenbeckSimulator:
    profiles = [
        ChannelProfile(
            channel=f"dummy_channel_{i}",
            unit="dummy_unit",
            sensor_type=SensorType.BME280,
            min_value=PROFILE_MIN,
            max_value=PROFILE_MAX,
            mean=PROFILE_MEAN,
            std_dev=PROFILE_STD,
        )
        for i in range(n_profiles)
    ]

    return OrnsteinUhlenbeckSimulator(DUMMY_DEVICE_ID, DUMMY_SENSOR_ID, profiles)

@pytest.mark.asyncio
async def test_read_returns_one_reading_per_profile():
    simulator = _make_simulator(n_profiles=3)
    readings  = await simulator.read()
    assert len(readings) == 3

@pytest.mark.asyncio
async def test_read_value_is_within_profile_bounds():
    simulator = _make_simulator()
    for _ in range(200):
        readings = await simulator.read()
        assert PROFILE_MIN <= readings[0].value <= PROFILE_MAX

@pytest.mark.asyncio
async def test_read_metadata_includes_alert_threshold():
    simulator = _make_simulator()
    readings  = await simulator.read()
    assert readings[0].metadata["alert_threshold"] == EXPECTED_ALERT_THRESHOLD

@pytest.mark.asyncio
async def test_read_metadata_simulation_type_is_ornstein_uhlenbeck():
    simulator = _make_simulator()
    readings  = await simulator.read()
    assert readings[0].metadata["simulation_type"] == "ornstein_uhlenbeck"

@pytest.mark.asyncio
async def test_initialize_and_close_complete_without_error():
    simulator = _make_simulator()
    await simulator.initialize()
    await simulator.close()

def test_blocks_on_read_is_false():
    simulator = _make_simulator()
    assert simulator.blocks_on_read is False