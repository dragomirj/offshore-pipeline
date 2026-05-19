# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] Cox-Ingersoll-Ross Process
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <13-May-2026>
# *****************************************************************************
import math
import random
from src.common.models.channel_profile import ChannelProfile

class CoxIngersollRossProcess:
    """Discrete-time simulation of a Cox-Ingersoll-Ross process for a single channel."""

    def __init__(self, profile: ChannelProfile):
        self._profile      = profile
        self._value        = max(profile.min_value, profile.mean + random.gauss(0, profile.std_dev))
        self._spike_ticks  = 0
        self._spike_target = 0.0

    def next(self) -> float:
        if self._spike_ticks > 0:
            effective_mean = self._spike_target
            self._spike_ticks -= 1
        elif random.random() < self._profile.spike_probability:
            self._spike_ticks  = self._profile.spike_duration_ticks
            # Spikes are upward-only: CIR models non-negative magnitudes where events are exceedances above baseline
            self._spike_target = self._profile.mean + self._profile.spike_magnitude_multiplier * self._profile.std_dev
            effective_mean     = self._spike_target
        else:
            effective_mean = self._profile.mean

        drift     = self._profile.mean_reversion_speed * (effective_mean - self._value)
        diffusion = self._profile.volatility * math.sqrt(max(self._value, 0.0)) * random.gauss(0, 1)
        self._value += drift + diffusion
        self._value  = max(self._profile.min_value, min(self._profile.max_value, self._value))
        return round(self._value, 3)

    @property
    def is_spiking(self) -> bool:
        return self._spike_ticks > 0
