# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Messaging Protocol Enum
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <11-Feb-2026>
# *****************************************************************************
from enum import Enum, unique

@unique
class MessagingProtocol(Enum):
    """
    Enum of messaging protocols for an event-driven, IoT-focused ETL system.
    Values are normalized to lowercase to ensure consistent identifiers across the codebase and configuration (e.g., YAML keys).
    """

    MQTT = 'mqtt'
    COAP = 'coap'
    HTTP = "http"

    @classmethod
    def parse(cls, value: str) -> "MessagingProtocol":
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"Expected string, got {type(value).__name__}")
        return cls(value.strip().lower())

    def __str__(self) -> str:
        """Return the lowercase value of the enum member."""
        return self.value