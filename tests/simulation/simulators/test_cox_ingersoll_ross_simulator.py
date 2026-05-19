# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] CIR Simulator Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <13-May-2026>
# *****************************************************************************
import pytest
from unittest.mock import AsyncMock, patch
from src.common.enums.sensor_type import SensorType
from src.common.models.channel_profile import ChannelProfile
from src.simulation.simulators.cox_ingersoll_ross_simulator import CoxIngersollRossSimulator

DUMMY_DEVICE_ID = "dummyDeviceId"
DUMMY_SENSOR_ID = "dummySensorId"
PROFILE_MIN = 0.0
PROFILE_MAX = 5.0
# Cox-Ingersoll-Ross (CIR) has a non-Gaussian (right-skewed) stationary distribution so alert_threshold is set explicitly
EXPECTED_ALERT_THRESHOLD = 4.0

def _make_simulator(n_profiles: int = 1, mean_interval_seconds: float = 1.0) -> CoxIngersollRossSimulator:
    profiles = [
        ChannelProfile(
            channel=f"dummy_channel_{i}",
            unit="dummy_unit",
            sensor_type=SensorType.ADXL345,
            min_value=PROFILE_MIN,
            max_value=PROFILE_MAX,
            mean=0.25,
            std_dev=0.1,
            alert_threshold=EXPECTED_ALERT_THRESHOLD,
        )
        for i in range(n_profiles)
    ]

    return CoxIngersollRossSimulator(DUMMY_DEVICE_ID, DUMMY_SENSOR_ID, profiles, mean_interval_seconds)

@pytest.mark.asyncio
async def test_read_returns_one_reading_per_profile():
    simulator = _make_simulator(n_profiles=3)
    with patch("asyncio.sleep", new_callable=AsyncMock):
        readings = await simulator.read()
    assert len(readings) == 3

@pytest.mark.asyncio
async def test_read_value_is_within_profile_bounds():
    simulator = _make_simulator()
    with patch("asyncio.sleep", new_callable=AsyncMock):
        for _ in range(200):
            readings = await simulator.read()
            assert PROFILE_MIN <= readings[0].value <= PROFILE_MAX

@pytest.mark.asyncio
async def test_read_metadata_includes_spiking():
    simulator = _make_simulator()
    with patch("asyncio.sleep", new_callable=AsyncMock):
        readings = await simulator.read()
    assert "spiking" in readings[0].metadata

@pytest.mark.asyncio
async def test_read_metadata_includes_alert_threshold():
    simulator = _make_simulator()
    with patch("asyncio.sleep", new_callable=AsyncMock):
        readings = await simulator.read()
    assert readings[0].metadata["alert_threshold"] == EXPECTED_ALERT_THRESHOLD

@pytest.mark.asyncio
async def test_read_metadata_simulation_type_is_cox_ingersoll_ross():
    simulator = _make_simulator()
    with patch("asyncio.sleep", new_callable=AsyncMock):
        readings = await simulator.read()
    assert readings[0].metadata["simulation_type"] == "cox_ingersoll_ross"

@pytest.mark.asyncio
async def test_read_sleeps_with_exponential_interval():
    simulator = _make_simulator(mean_interval_seconds=2.0)
    with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep, \
         patch("random.expovariate", return_value=1.5):
        await simulator.read()
    mock_sleep.assert_awaited_once_with(1.5)

@pytest.mark.asyncio
async def test_initialize_and_close_complete_without_error():
    simulator = _make_simulator()
    await simulator.initialize()
    await simulator.close()

def test_blocks_on_read_is_true():
    simulator = _make_simulator()
    assert simulator.blocks_on_read is True
