# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] Simulation Metadata Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <11-May-2026>
# *****************************************************************************
from src.simulation.metadata import simulation_metadata

def test_simulation_metadata_sets_simulation_type():
    result = simulation_metadata("constant_mean", alert_threshold=51.0, spiking=False)
    assert result["simulation_type"] == "constant_mean"

def test_simulation_metadata_includes_spiking_when_false():
    result = simulation_metadata("constant_mean", alert_threshold=51.0, spiking=False)
    assert result["spiking"] is False

def test_simulation_metadata_includes_spiking_when_true():
    result = simulation_metadata("constant_mean", alert_threshold=51.0, spiking=True)
    assert result["spiking"] is True
