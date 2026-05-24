# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] No Encryption Cipher
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <19-May-2026>
# *****************************************************************************
from __future__ import annotations
from src.common.enums.encryption_scheme import EncryptionScheme
from src.common.crypto.cipher.base import PayloadCipher

class NoEncryptionCipher(PayloadCipher):
    """Passthrough cipher. Not for production use."""

    @property
    def scheme(self) -> EncryptionScheme:
        return EncryptionScheme.NO_ENCRYPTION

    def encrypt(self, plaintext: bytes) -> bytes:
        return plaintext

    def decrypt(self, ciphertext: bytes) -> bytes:
        return ciphertext
