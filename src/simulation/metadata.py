# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] Simulation Metadata
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <09-May-2026>
# *****************************************************************************
from src.common.models.sensor_reading import Metadata, MetadataValue

def simulation_metadata(simulation_type: str, **kwargs: MetadataValue) -> Metadata:
    """Return metadata for a synthetic reading, always including 'synthetic' and 'simulation_type'."""
    return {
        "synthetic": True,
        "simulation_type": simulation_type,
        **kwargs,
    }