# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Protobuf Serializer
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <21-May-2026>
# *****************************************************************************
from __future__ import annotations
from types import MappingProxyType
from src.common.enums.serialization_format import SerializationFormat
from src.common.models.sensor_event import (
    ChannelMetadata, Device, Location, SensorEvent, SimulationInfo, Trace,
)
from google.protobuf.message import DecodeError
from src.common.serialization.base import PayloadSerializer
from src.common.serialization.errors import (
    MalformedPayloadError,
    SchemaViolationError,
)
from src.common.serialization.serializers.protobuf.proto import sensor_event_pb2

class ProtobufSerializer(PayloadSerializer):
    """
    Serializes payloads using Protocol Buffers (binary format).

    - Supported in all environments.
    - Required in development, staging, and production.
    - Produces compact payloads and enforces a strict schema.
    """

    @property
    def format(self) -> SerializationFormat:
        return SerializationFormat.PROTOBUF
    
    def serialize(self, event: SensorEvent) -> bytes:
        pb = sensor_event_pb2.SensorEvent(
            occurred_at=event.occurred_at,
            ingested_at=event.ingested_at,
            device=sensor_event_pb2.Device(
                device_id=event.device.device_id,
                sensor_id=event.device.sensor_id,
                firmware_version=event.device.firmware_version,
                location=sensor_event_pb2.Location(
                    lat=event.device.location.lat,
                    lon=event.device.location.lon,
                ),
            ),
            data=event.data,
            channels={
                channel: sensor_event_pb2.ChannelMetadata(
                    spiking=metadata.spiking,
                    alert_threshold=metadata.alert_threshold,
                )
                for channel, metadata in event.channels.items()
            },
            trace=sensor_event_pb2.Trace(
                event_id=event.trace.event_id,
                trace_id=event.trace.trace_id,
                span_id=event.trace.span_id,
            ),
            tags=event.tags,
            simulation=sensor_event_pb2.SimulationInfo(
                simulation_type=event.simulation.simulation_type,
            ) if event.simulation is not None else None,
        )

        return pb.SerializeToString()  # type: ignore[no-any-return]

    def deserialize(self, data: bytes) -> SensorEvent:
        pb = sensor_event_pb2.SensorEvent()
        try:
            pb.ParseFromString(data)
        except DecodeError as exc:
            raise MalformedPayloadError("Invalid protobuf payload") from exc

        location = Location(
            lat=float(pb.device.location.lat),
            lon=float(pb.device.location.lon),
        )

        event_channels: dict[str, ChannelMetadata] = {
            str(channel): ChannelMetadata(
                spiking=bool(metadata.spiking),
                alert_threshold=float(metadata.alert_threshold),
            )
            for channel, metadata in pb.channels.items()
        }
        simulation: SimulationInfo | None = None
        if pb.HasField("simulation"):
            simulation = SimulationInfo(
                simulation_type=str(pb.simulation.simulation_type),
            )

        try:
            return SensorEvent(
                occurred_at=int(pb.occurred_at),
                ingested_at=int(pb.ingested_at),
                device=Device(
                    device_id=str(pb.device.device_id),
                    sensor_id=str(pb.device.sensor_id),
                    firmware_version=str(pb.device.firmware_version),
                    location=location,
                ),
                data=MappingProxyType({str(k): float(v) for k, v in pb.data.items()}),
                channels=MappingProxyType(event_channels),
                trace=Trace(
                    event_id=str(pb.trace.event_id),
                    trace_id=str(pb.trace.trace_id),
                    span_id=str(pb.trace.span_id),
                ),
                tags=tuple(str(t) for t in pb.tags),
                simulation=simulation,
            )
        except ValueError as exc:
            raise SchemaViolationError(str(exc)) from exc