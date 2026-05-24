# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] No Encryption Cipher Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <23-May-2026>
# *****************************************************************************
from src.common.crypto.cipher.no_encryption_cipher import NoEncryptionCipher
from src.common.enums.encryption_scheme import EncryptionScheme

def test_encrypt_returns_plaintext_unchanged():
    cipher = NoEncryptionCipher()
    plaintext = b"some dummy sensitive data"
    assert cipher.encrypt(plaintext) == plaintext

def test_decrypt_returns_ciphertext_unchanged():
    cipher = NoEncryptionCipher()
    data = b"some dummy sensitive data"
    assert cipher.decrypt(data) == data

def test_roundtrip_handles_empty_payload():
    cipher = NoEncryptionCipher()
    assert cipher.decrypt(cipher.encrypt(b"")) == b""

def test_scheme_is_no_encryption():
    assert NoEncryptionCipher().scheme == EncryptionScheme.NO_ENCRYPTION
