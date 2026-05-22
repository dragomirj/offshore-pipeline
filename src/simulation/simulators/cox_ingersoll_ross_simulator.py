# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] Cox-Ingersoll-Ross Simulator
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <13-May-2026>
# *****************************************************************************
import asyncio
import random
from src.common.models.sensor_reading import SensorReading
from src.common.models.channel_profile import ChannelProfile
from src.simulation.metadata import simulation_metadata
from src.simulation.processes.cox_ingersoll_ross_process import CoxIngersollRossProcess

class CoxIngersollRossSimulator:
    """
    Simulates a Cox-Ingersoll-Ross (CIR) process, a mean-reverting stochastic process for non-negative magnitudes.
    The square-root diffusion keeps values non-negative and scales noise with the current level,
    producing less variation in quiet periods and more in energetic ones.
    """

    def __init__(self, device_id: str, sensor_id: str, profiles: list[ChannelProfile], mean_interval_seconds: float = 1.0):
        self._device_id = device_id
        self._sensor_id = sensor_id
        self._profiles  = profiles
        self._interval  = mean_interval_seconds
        self._processes = {p.channel: CoxIngersollRossProcess(p) for p in profiles}

    async def initialize(self) -> None:
        pass  # no warmup, no hardware

    async def read(self) -> list[SensorReading]:
        await asyncio.sleep(random.expovariate(1.0 / self._interval))
        readings: list[SensorReading] = []
        for p in self._profiles:
            value   = self._processes[p.channel].next()
            spiking = value > p.alert_threshold
            readings.append(
                SensorReading(
                    device_id=self._device_id,
                    sensor_id=self._sensor_id,
                    sensor_type=p.sensor_type,
                    channel=p.channel,
                    value=value,
                    unit=p.unit,
                    metadata=simulation_metadata(
                        "cox_ingersoll_ross",
                        alert_threshold=p.alert_threshold,
                        spiking=spiking,
                )
            )
        )

        return readings

    async def close(self) -> None:
        pass

    @property
    def blocks_on_read(self) -> bool:
        return True
