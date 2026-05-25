# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] JSON Serializer
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <21-May-2026>
# *****************************************************************************
from __future__ import annotations
import json
from types import MappingProxyType
from typing import Any, Mapping
from src.common.enums.serialization_format import SerializationFormat
from src.common.models.sensor_event import (
    ChannelMetadata, Device, Location, SensorEvent, SimulationInfo, Trace,
)
from src.common.serialization.base import PayloadSerializer
from src.common.serialization.errors import (
    MalformedPayloadError,
    MissingFieldError,
    SchemaViolationError,
)

def _require(mapping: Mapping[str, Any], key: str, path: str) -> Any:
    if key not in mapping:
        raise MissingFieldError(f"Missing required field: {path}")
    return mapping[key]

class JsonSerializer(PayloadSerializer):
    """
    Serializes payloads using JSON format.

    - Supported in simulation environment only.
    - Human-readable and easy to inspect.
    - Does not enforce a schema, so deserialize() validates required fields explicitly.
    """

    @property
    def format(self) -> SerializationFormat:
        return SerializationFormat.JSON

    def serialize(self, event: SensorEvent) -> bytes:
        obj: dict[str, object] = {
            "occurred_at": event.occurred_at,
            "ingested_at": event.ingested_at,
            "device": {
                "device_id": event.device.device_id,
                "sensor_id": event.device.sensor_id,
                "firmware_version": event.device.firmware_version,
                "location": {
                    "lat": event.device.location.lat,
                    "lon": event.device.location.lon,
                },
            },
            "data": dict(event.data),
            "channels": {
                channel: {
                    "spiking": metadata.spiking,
                    "alert_threshold": metadata.alert_threshold,
                }
                for channel, metadata in event.channels.items()
            },
            "trace": {
                "event_id": event.trace.event_id,
                "trace_id": event.trace.trace_id,
                "span_id": event.trace.span_id,
            },
            "tags": event.tags,
        }

        if event.simulation is not None:
            obj["simulation"] = {
                "simulation_type": event.simulation.simulation_type,
            }

        return json.dumps(obj, separators=(",", ":"), sort_keys=True).encode("utf-8")

    def deserialize(self, data: bytes) -> SensorEvent:
        try:
            raw = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise MalformedPayloadError("Invalid JSON payload") from exc

        raw_device     = _require(raw, "device", "device")
        raw_location   = _require(raw_device, "location", "device.location")
        raw_trace      = _require(raw, "trace", "trace")
        raw_channels   = _require(raw, "channels", "channels")
        raw_simulation = raw.get("simulation")

        try:
            event_channels: dict[str, ChannelMetadata] = {
                channel: ChannelMetadata(
                    spiking=bool(_require(metadata, "spiking", f"channels.{channel}.spiking")),
                    alert_threshold=float(
                        _require(metadata, "alert_threshold", f"channels.{channel}.alert_threshold")
                    ),
                )
                for channel, metadata in raw_channels.items()
            }
            simulation: SimulationInfo | None = None
            if raw_simulation is not None:
                simulation = SimulationInfo(
                    simulation_type=str(_require(raw_simulation, "simulation_type", "simulation.simulation_type")),
                )

            return SensorEvent(
                occurred_at=int(_require(raw, "occurred_at", "occurred_at")),
                ingested_at=int(_require(raw, "ingested_at", "ingested_at")),
                device=Device(
                    device_id=str(_require(raw_device, "device_id", "device.device_id")),
                    sensor_id=str(_require(raw_device, "sensor_id", "device.sensor_id")),
                    firmware_version=str(_require(raw_device, "firmware_version", "device.firmware_version")),
                    location=Location(
                        lat=float(_require(raw_location, "lat", "device.location.lat")),
                        lon=float(_require(raw_location, "lon", "device.location.lon")),
                    ),
                ),
                data=MappingProxyType({
                    str(k): float(v)
                    for k, v in _require(raw, "data", "data").items()
                }),
                channels=MappingProxyType(event_channels),
                trace=Trace(
                    event_id=str(_require(raw_trace, "event_id", "trace.event_id")),
                    trace_id=str(_require(raw_trace, "trace_id", "trace.trace_id")),
                    span_id=str(_require(raw_trace, "span_id", "trace.span_id")),
                ),
                tags=tuple(str(t) for t in _require(raw, "tags", "tags")),
                simulation=simulation,
            )
        except (ValueError, TypeError) as exc:
            raise SchemaViolationError(str(exc)) from exc
