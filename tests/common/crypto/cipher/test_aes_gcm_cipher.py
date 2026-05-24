# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] AES-GCM Cipher Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <23-May-2026>
# *****************************************************************************
import os
import pytest
from cryptography.exceptions import InvalidTag
from src.common.crypto.cipher.aes_gcm_cipher import AesGcmCipher
from src.common.enums.encryption_scheme import EncryptionScheme

def _key_hex() -> str:
    return os.urandom(32).hex()

def test_roundtrip_recovers_plaintext():
    cipher = AesGcmCipher(_key_hex())
    plaintext = b"some dummy sensitive data"
    assert cipher.decrypt(cipher.encrypt(plaintext)) == plaintext

def test_roundtrip_handles_empty_payload():
    cipher = AesGcmCipher(_key_hex())
    assert cipher.decrypt(cipher.encrypt(b"")) == b""

def test_roundtrip_handles_large_payload():
    cipher = AesGcmCipher(_key_hex())
    plaintext = os.urandom(64 * 1024)
    assert cipher.decrypt(cipher.encrypt(plaintext)) == plaintext

def test_distinct_nonce_per_encrypt():
    cipher = AesGcmCipher(_key_hex())
    plaintext = b"some dummy sensitive data"
    a = cipher.encrypt(plaintext)
    b = cipher.encrypt(plaintext)
    assert a != b
    assert a[:AesGcmCipher.NONCE_BYTES] != b[:AesGcmCipher.NONCE_BYTES]

def test_short_key_raises_on_construction():
    with pytest.raises(ValueError, match="32-byte key"):
        AesGcmCipher(os.urandom(16).hex())

def test_long_key_raises_on_construction():
    with pytest.raises(ValueError, match="32-byte key"):
        AesGcmCipher(os.urandom(64).hex())

def test_tampered_ciphertext_raises_on_decrypt():
    cipher = AesGcmCipher(_key_hex())
    ciphertext = bytearray(cipher.encrypt(b"some dummy sensitive data"))
    ciphertext[-1] ^= 0xFF  # flip last byte of GCM tag
    with pytest.raises(InvalidTag):
        cipher.decrypt(bytes(ciphertext))

def test_truncated_ciphertext_raises():
    cipher = AesGcmCipher(_key_hex())
    with pytest.raises(ValueError, match="too short"):
        cipher.decrypt(b"\x00" * (AesGcmCipher.NONCE_BYTES - 1))

def test_scheme_is_aes_gcm():
    assert AesGcmCipher(_key_hex()).scheme == EncryptionScheme.AES_GCM
