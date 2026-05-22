# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] Constant Simulator
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <19-Feb-2026>
# *****************************************************************************
from src.common.models.sensor_reading import SensorReading
from src.common.models.channel_profile import ChannelProfile
from src.simulation.metadata import simulation_metadata

class ConstantSimulator:
    """
    Simulates a constant process where every channel is fixed at its mean with no noise or drift.
    Drop-in replacement for OrnsteinUhlenbeckSimulator in SimulationFactory.create_polled
    for testing and for scenarios where constant baseline data is required.
    """
    
    def __init__(self, device_id: str, sensor_id: str, profiles: list[ChannelProfile]):
        self._device_id = device_id
        self._sensor_id = sensor_id
        self._profiles  = profiles

    async def initialize(self) -> None:
        pass  # no warmup, no hardware

    async def read(self) -> list[SensorReading]:
        return [
            SensorReading(                
                device_id=self._device_id,
                sensor_id=self._sensor_id, 
                sensor_type=p.sensor_type, 
                channel=p.channel,
                value=p.mean,
                unit=p.unit,
                metadata=simulation_metadata(
                    "constant_mean",
                    alert_threshold=p.alert_threshold,
                    spiking=False,
                ),
            )
            for p in self._profiles
        ]
    
    async def close(self) -> None:
        pass

    @property
    def blocks_on_read(self) -> bool:
        return False