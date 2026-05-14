# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Base Enum Class
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <04-May-2026>
# ***************************************************************************** 
from enum import Enum

class ParsableEnum(Enum):
    @classmethod
    def parse(cls, value: str):
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"Expected string, got {type(value).__name__}")

        try:
            return cls(value.strip().lower())
        except ValueError:
            raise ValueError(f"Invalid {cls.__name__}: {value!r}") from None

    def __str__(self) -> str:
        return self.value