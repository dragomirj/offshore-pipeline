# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] ChaCha20-Poly1305 Cipher
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <19-May-2026>
# *****************************************************************************
from __future__ import annotations
import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from src.common.enums.encryption_scheme import EncryptionScheme
from src.common.crypto.cipher.base import PayloadCipher

class ChaCha20Poly1305Cipher(PayloadCipher):
    # Prefer on devices without AES hardware (e.g. ESP32, STM32, bare Cortex-M).
    # Nonce is fresh-random per encrypt(); reusing a nonce with the same key is unsafe.
    NONCE_BYTES = 12
    KEY_BYTES   = 32

    def __init__(self, key_hex: str) -> None:
        # Key is loaded from .env (not secure, showcase only); production should use AWS KMS, Azure Key Vault, or HashiCorp Vault.
        key = bytes.fromhex(key_hex)
        if len(key) != self.KEY_BYTES:
            raise ValueError(
                f"ChaCha20Poly1305Cipher requires a {self.KEY_BYTES}-byte key ({self.KEY_BYTES * 2} hex chars), got {len(key)} bytes."
            )
        
        self._aead = ChaCha20Poly1305(key)

    @property
    def scheme(self) -> EncryptionScheme:
        return EncryptionScheme.CHACHA20_POLY1305

    def encrypt(self, plaintext: bytes) -> bytes:
        nonce = os.urandom(self.NONCE_BYTES)
        return nonce + self._aead.encrypt(nonce, plaintext, None)

    def decrypt(self, ciphertext: bytes) -> bytes:
        if len(ciphertext) < self.NONCE_BYTES:
            raise ValueError("Ciphertext too short to contain a nonce.")
        nonce, body = ciphertext[:self.NONCE_BYTES], ciphertext[self.NONCE_BYTES:]
        return self._aead.decrypt(nonce, body, None)
