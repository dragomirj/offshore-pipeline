# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Cipher Base
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <19-May-2026>
# *****************************************************************************
from __future__ import annotations
from abc import ABC, abstractmethod
from src.common.enums.encryption_scheme import EncryptionScheme

class PayloadCipher(ABC):
    @property
    @abstractmethod
    def scheme(self) -> EncryptionScheme: ...

    @abstractmethod
    def encrypt(self, plaintext: bytes) -> bytes: ...

    @abstractmethod
    def decrypt(self, ciphertext: bytes) -> bytes: ...
