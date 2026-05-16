# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Encryption Scheme Enum
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <04-May-2026>
# ***************************************************************************** 
from enum import unique
from src.common.enums.base import ParsableEnum

@unique
class EncryptionScheme(ParsableEnum):
    """
    Encryption schemes for sensor events.

    - NONE: Permitted in SIMULATION and DEVELOPMENT. Prohibited in STAGING and PRODUCTION.
      See: DeploymentEnvironment.requires_encryption()

    - AES_GCM / CHACHA20_POLY1305: Permitted in all environments.
    """

    NONE              = "none"
    AES_GCM           = "aes_gcm"
    CHACHA20_POLY1305 = "chacha20_poly1305"