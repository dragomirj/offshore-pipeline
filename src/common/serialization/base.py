# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Serialization Base
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <21-May-2026>
# *****************************************************************************
from __future__ import annotations
from abc import ABC, abstractmethod
from src.common.enums.serialization_format import SerializationFormat
from src.common.models.sensor_event import SensorEvent

class PayloadSerializer(ABC):
    """Abstract base for SensorEvent serialization."""

    @property
    @abstractmethod
    def format(self) -> SerializationFormat: ...

    @abstractmethod
    def serialize(self, event: SensorEvent) -> bytes: ...

    @abstractmethod
    def deserialize(self, data: bytes) -> SensorEvent: ...
