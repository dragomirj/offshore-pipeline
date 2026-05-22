# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] Simulation Metadata
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <09-May-2026>
# *****************************************************************************
from src.common.models.sensor_reading import Metadata, MetadataValue

def simulation_metadata(simulation_type: str, alert_threshold: float, spiking: bool, **kwargs: MetadataValue) -> Metadata:
    """Return metadata for a synthetic reading, always including 'simulation_type', 'alert_threshold' and 'spiking'."""
    return {
        "simulation_type": simulation_type,
        "alert_threshold": alert_threshold,
        "spiking": spiking,
        **kwargs,
    }