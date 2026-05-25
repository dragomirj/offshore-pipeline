# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Serialization Errors
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <21-May-2026>
# *****************************************************************************
from __future__ import annotations

class SerializationError(Exception):
    """Base for all serialization/deserialization failures."""

class MalformedPayloadError(SerializationError):
    """Raw bytes could not be parsed as the expected wire format."""

class MissingFieldError(SerializationError):
    """A required field was absent from the payload."""

class SchemaViolationError(SerializationError):
    """Parsed payload violates a model invariant."""
