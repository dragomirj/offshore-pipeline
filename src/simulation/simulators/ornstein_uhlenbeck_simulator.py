# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] Ornstein-Uhlenbeck Simulator
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <19-Feb-2026>
# *****************************************************************************
from src.common.models.sensor_reading import SensorReading
from src.common.models.channel_profile import ChannelProfile
from src.simulation.metadata import simulation_metadata
from src.simulation.processes.ornstein_uhlenbeck_process import OrnsteinUhlenbeckProcess

class OrnsteinUhlenbeckSimulator:
    """
    Simulates an Ornstein-Uhlenbeck (OU) process, a mean-reverting stochastic process.
    The state evolves with random noise but is continuously pulled toward a long-term mean, 
    producing temporally correlated (smooth) fluctuations rather than an unbounded random walk.
    """
    
    def __init__(self, device_id: str, sensor_id: str, profiles: list[ChannelProfile]):
        self._device_id = device_id
        self._sensor_id = sensor_id
        self._profiles  = profiles
        self._processes = {p.channel: OrnsteinUhlenbeckProcess(p) for p in profiles}

    async def initialize(self) -> None:
        pass  # no warmup, no hardware

    async def read(self) -> list[SensorReading]:
        return [
            SensorReading(
                device_id=self._device_id,
                sensor_id=self._sensor_id,
                sensor_type=p.sensor_type,
                channel=p.channel,
                value=self._processes[p.channel].next(),
                unit=p.unit,
                metadata=simulation_metadata(
                    "ornstein_uhlenbeck",
                    spiking=self._processes[p.channel].is_spiking,
                    alert_threshold=p.alert_threshold,
                ),
            )
            for p in self._profiles
        ]

    async def close(self) -> None:
        pass

    @property
    def blocks_on_read(self) -> bool:
        return False