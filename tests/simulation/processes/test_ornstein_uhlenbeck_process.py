# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] OU Process Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <11-May-2026>
# *****************************************************************************
from src.common.enums.sensor_type import SensorType
from src.common.models.channel_profile import ChannelProfile
from src.simulation.processes.ornstein_uhlenbeck_process import OrnsteinUhlenbeckProcess

PROFILE_MIN = 0.0
PROFILE_MAX = 100.0
PROFILE_MEAN = 50.0
PROFILE_STD_DEV = 5.0
PROFILE_MEAN_REVERSION_SPEED = 0.1
PROFILE_SPIKE_MAGNITUDE_MULTIPLIER = 3.0
PROFILE_VOLATILITY = 1.0

def _make_process(spike_probability: float = 0.0, spike_duration: int = 5) -> OrnsteinUhlenbeckProcess:
    profile = ChannelProfile(
        channel="dummy_channel",
        unit="dummy_unit",
        sensor_type=SensorType.BME280,
        min_value=PROFILE_MIN,
        max_value=PROFILE_MAX,
        mean=PROFILE_MEAN,
        std_dev=PROFILE_STD_DEV,
        mean_reversion_speed=PROFILE_MEAN_REVERSION_SPEED,
        volatility=PROFILE_VOLATILITY,
        spike_probability=spike_probability,
        spike_magnitude_multiplier=PROFILE_SPIKE_MAGNITUDE_MULTIPLIER,
        spike_duration_ticks=spike_duration,
    )

    return OrnsteinUhlenbeckProcess(profile)

def test_next_value_always_within_bounds():
    process = _make_process()
    for _ in range(200):
        value = process.next()
        assert PROFILE_MIN <= value <= PROFILE_MAX

def test_is_spiking_starts_false():
    process = _make_process()
    assert process.is_spiking is False

def test_is_spiking_becomes_true_after_spike_starts():
    process = _make_process(spike_probability=1.0, spike_duration=5)
    process.next()
    assert process.is_spiking is True

def test_spike_branch_executes_during_active_spike():
    # First next() triggers the spike, second next() hits the ticks > 0 branch
    process = _make_process(spike_probability=1.0, spike_duration=5)
    process.next()
    process.next()
    assert process.is_spiking is True

def test_is_spiking_false_with_zero_spike_probability():
    process = _make_process(spike_probability=0.0)
    for _ in range(200):
        process.next()
    assert process.is_spiking is False