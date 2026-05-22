# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [EVENTS] Event Assembler
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <09-May-2026>
# *****************************************************************************
from __future__ import annotations
import time
from dataclasses import dataclass
from types import MappingProxyType
from typing import cast
from src.common.models.sensor_event import ChannelMetadata, Device, Location, SensorEvent, SimulationInfo
from src.common.models.sensor_reading import SensorReading

@dataclass(frozen=True)
class AssemblerConfig:
    firmware_version: str
    location:         Location
    tags:             tuple[str, ...]

class EventAssembler:
    """
    Assembles list[SensorReading] into a single SensorEvent.
    Does NOT serialize. Does NOT encrypt. Those responsibilities belong to later pipeline stages.
    All readings in a batch are expected to originate from the same device and sensor.
    """

    def __init__(self, config: AssemblerConfig) -> None:
        self._config = config

    def assemble(self, readings: list[SensorReading]) -> SensorEvent:
        """Assembles one sensor tick into one SensorEvent."""
        if not readings:
            raise ValueError("Cannot assemble SensorEvent from empty readings list.")

        occurred_at = int(min(r.timestamp for r in readings).timestamp() * 1000)
        ingested_at = int(time.time_ns() // 1_000_000)
        channels = MappingProxyType({
            r.channel: ChannelMetadata(
                spiking=cast(bool, r.metadata.get("spiking", False)),
                alert_threshold=cast(float, r.metadata["alert_threshold"]),
            )
            for r in readings
        })

        simulation_type = next((r.metadata["simulation_type"] for r in readings if "simulation_type" in r.metadata), None)
        simulation = SimulationInfo(simulation_type=str(simulation_type)) if simulation_type is not None else None

        return SensorEvent(
            occurred_at=occurred_at,
            ingested_at=ingested_at,
            device=Device(
                device_id=readings[0].device_id,
                sensor_id=readings[0].sensor_id,
                firmware_version=self._config.firmware_version,
                location=self._config.location,
            ),
            data=MappingProxyType({r.channel: r.value for r in readings}),
            channels=channels,
            tags=self._config.tags,
            simulation=simulation,
        )
