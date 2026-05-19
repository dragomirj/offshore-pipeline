# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] CIR Process Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <13-May-2026>
# *****************************************************************************
from src.common.enums.sensor_type import SensorType
from src.common.models.channel_profile import ChannelProfile
from src.simulation.processes.cox_ingersoll_ross_process import CoxIngersollRossProcess

PROFILE_MIN  = 0.0
PROFILE_MAX  = 5.0
PROFILE_MEAN = 0.25

def _make_process(spike_probability: float = 0.0, spike_duration: int = 5) -> CoxIngersollRossProcess:
    profile = ChannelProfile(
        channel="dummy_channel",
        unit="dummy_unit",
        sensor_type=SensorType.ADXL345,
        min_value=PROFILE_MIN,
        max_value=PROFILE_MAX,
        mean=PROFILE_MEAN,
        std_dev=0.1,
        mean_reversion_speed=0.15,
        volatility=0.11,
        spike_probability=spike_probability,
        spike_magnitude_multiplier=5.0,
        spike_duration_ticks=spike_duration,
        alert_threshold=4.0,
    )

    return CoxIngersollRossProcess(profile)

def test_next_value_always_within_bounds():
    process = _make_process()
    for _ in range(200):
        value = process.next()
        assert PROFILE_MIN <= value <= PROFILE_MAX

def test_next_value_always_non_negative():
    # Square-root diffusion and Feller condition keep values >= 0
    process = _make_process()
    for _ in range(200):
        assert process.next() >= 0.0

def test_is_spiking_starts_false():
    assert _make_process().is_spiking is False

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

def test_spike_target_is_always_above_mean():
    # CIR spikes are unidirectional, always above mean
    process = _make_process(spike_probability=1.0, spike_duration=5)
    process.next()
    assert process._spike_target > PROFILE_MEAN  # pyright: ignore[reportPrivateUsage]
