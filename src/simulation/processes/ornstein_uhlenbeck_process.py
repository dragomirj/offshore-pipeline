# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] Ornstein-Uhlenbeck Process
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <19-Feb-2026>
# ***************************************************************************** 
import random, math
from src.common.models.channel_profile import ChannelProfile

class OrnsteinUhlenbeckProcess:
    def __init__(self, profile: ChannelProfile):
        self._profile      = profile
        self._value        = profile.mean + random.gauss(0, profile.std_dev)
        self._spike_ticks  = 0
        self._spike_target = 0.0

    def next(self) -> float:
        if self._spike_ticks > 0:
            effective_mean = self._spike_target
            self._spike_ticks -= 1
        elif random.random() < self._profile.spike_probability:
            self._spike_ticks  = self._profile.spike_duration_ticks
            self._spike_target = self._profile.mean + random.choice([-1,1]) * self._profile.spike_magnitude_multiplier * self._profile.std_dev
            effective_mean     = self._spike_target
        else:
            effective_mean = self._profile.mean

        drift = self._profile.mean_reversion_speed * (effective_mean - self._value)
        noise = self._profile.volatility * math.sqrt(1.0) * random.gauss(0, 1)
        self._value += drift + noise
        self._value  = max(self._profile.min_value, min(self._profile.max_value, self._value))
        return round(self._value, 3)

    @property
    def is_spiking(self) -> bool:
        return self._spike_ticks > 0