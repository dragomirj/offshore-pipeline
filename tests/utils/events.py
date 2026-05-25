# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [UTILS] Event Utils
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <25-May-2026>
# *****************************************************************************
from types import MappingProxyType
from src.common.models.sensor_event import (
    ChannelMetadata, Device, Location, SensorEvent, SimulationInfo, Trace,
)

def create_dummy_event(simulation: SimulationInfo | None = None) -> SensorEvent:
    return SensorEvent(
        occurred_at=1_000_000,
        ingested_at=1_000_001,
        device=Device(
            device_id="dummyDeviceId",
            sensor_id="dummySensorId",
            firmware_version="1.0.0",
            location=Location(lat=44.823083, lon=20.447571),
        ),
        data=MappingProxyType({"co_ppm": 12.5}),
        channels=MappingProxyType({
            "co_ppm": ChannelMetadata(spiking=False, alert_threshold=200.0),
        }),
        trace=Trace(
            event_id="00000000-0000-0000-0000-000000000001",
            trace_id="aabbccddeeff00112233445566778899",
            span_id="aabbccdd11223344",
        ),
        tags=("test", "dummy"),
        simulation=simulation,
    )
