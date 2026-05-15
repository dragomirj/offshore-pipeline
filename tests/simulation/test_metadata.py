# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] Simulation Metadata Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <11-May-2026>
# *****************************************************************************
from src.simulation.metadata import simulation_metadata

def test_simulation_metadata_sets_synthetic_true():
    result = simulation_metadata("ornstein_uhlenbeck")
    assert result["synthetic"] is True

def test_simulation_metadata_sets_simulation_type():
    result = simulation_metadata("constant_mean")
    assert result["simulation_type"] == "constant_mean"

def test_simulation_metadata_merges_kwargs():
    result = simulation_metadata("ornstein_uhlenbeck", spiking=True, alert_threshold=100.0)
    assert result["spiking"] is True
    assert result["alert_threshold"] == 100.0