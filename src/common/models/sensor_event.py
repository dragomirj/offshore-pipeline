# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Sensor Event Models
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <09-May-2026>
# *****************************************************************************
from __future__ import annotations
import secrets
import uuid
from dataclasses import dataclass, field
from types import MappingProxyType

@dataclass(frozen=True)
class Location:
    lat: float
    lon: float

@dataclass(frozen=True)
class Device:
    device_id:        str
    sensor_id:        str
    firmware_version: str
    location:         Location

@dataclass(frozen=True)
class Trace:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = field(default_factory=lambda: secrets.token_hex(16))
    span_id:  str = field(default_factory=lambda: secrets.token_hex(8))

@dataclass(frozen=True)
class ChannelMetadata:
    spiking:         bool
    alert_threshold: float

@dataclass(frozen=True)
class SimulationInfo:
    simulation_type: str

@dataclass(frozen=True)
class SensorEvent:
    occurred_at: int  # unix millis
    ingested_at: int  # unix millis
    device:      Device
    data:        MappingProxyType[str, float]
    channels:    MappingProxyType[str, ChannelMetadata]
    trace:       Trace = field(default_factory=Trace)
    tags:        tuple[str, ...] = field(default_factory=tuple)
    simulation:  SimulationInfo | None = None
