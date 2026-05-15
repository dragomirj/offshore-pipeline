# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] Simulation Factory Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <01-May-2026>
# *****************************************************************************
import pytest
from src.common.enums.sensor_type import SensorType
from src.common.models.channel_profile import ChannelProfile
from src.simulation.factory import SimulationFactory, SimulationInProductionError
from src.simulation.simulators.constant_simulator import ConstantSimulator
from src.simulation.simulators.ornstein_uhlenbeck_simulator import OrnsteinUhlenbeckSimulator

DUMMY_DEVICE_ID = "dummyDeviceId"
DUMMY_SENSOR_ID = "dummySensorId"

def _make_profile(sensor_type: SensorType) -> ChannelProfile:
    return ChannelProfile(
        channel="dummy_channel",
        unit="dummy_unit",
        sensor_type=sensor_type,
        min_value=-10.0,
        max_value=50.0,
        mean=22.0,
        std_dev=1.5,
    )

def test_create_ornstein_uhlenbeck_returns_ou_simulator_in_simulation_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DEPLOYMENT_ENVIRONMENT", raising=False)
    profile = _make_profile(SensorType.BME280)
    monkeypatch.setattr(SimulationFactory, "_registry", {SensorType.BME280: [profile]}, raising=False)

    simulator = SimulationFactory.create_ornstein_uhlenbeck(DUMMY_DEVICE_ID, DUMMY_SENSOR_ID, SensorType.BME280)

    assert isinstance(simulator, OrnsteinUhlenbeckSimulator)

def test_create_constant_returns_constant_simulator_in_simulation_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DEPLOYMENT_ENVIRONMENT", raising=False)
    profile = _make_profile(SensorType.BME280)
    monkeypatch.setattr(SimulationFactory, "_registry", {SensorType.BME280: [profile]}, raising=False)

    simulator = SimulationFactory.create_constant(DUMMY_DEVICE_ID, DUMMY_SENSOR_ID, SensorType.BME280)

    assert isinstance(simulator, ConstantSimulator)

def test_create_constant_returns_constant_simulator_in_development_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DEPLOYMENT_ENVIRONMENT", "development")
    profile = _make_profile(SensorType.BME280)
    monkeypatch.setattr(SimulationFactory, "_registry", {SensorType.BME280: [profile]}, raising=False)

    simulator = SimulationFactory.create_constant(DUMMY_DEVICE_ID, DUMMY_SENSOR_ID, SensorType.BME280)

    assert isinstance(simulator, ConstantSimulator)

def test_create_ornstein_uhlenbeck_raises_when_sensor_type_not_registered(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DEPLOYMENT_ENVIRONMENT", raising=False)
    monkeypatch.setattr(SimulationFactory, "_registry", {}, raising=False)

    with pytest.raises(ValueError, match="No simulation profiles"):
        SimulationFactory.create_ornstein_uhlenbeck(DUMMY_DEVICE_ID, DUMMY_SENSOR_ID, SensorType.BME280)

def test_create_constant_raises_when_sensor_type_not_registered(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DEPLOYMENT_ENVIRONMENT", raising=False)
    monkeypatch.setattr(SimulationFactory, "_registry", {}, raising=False)

    with pytest.raises(ValueError, match="No simulation profiles"):
        SimulationFactory.create_constant(DUMMY_DEVICE_ID, DUMMY_SENSOR_ID, SensorType.BME280)

@pytest.mark.parametrize("env", ["production"])
def test_factory_raises_in_disallowed_environments(monkeypatch: pytest.MonkeyPatch, env: str):
    monkeypatch.setenv("DEPLOYMENT_ENVIRONMENT", env)
    profile = _make_profile(SensorType.BME280)
    monkeypatch.setattr(SimulationFactory, "_registry", {SensorType.BME280: [profile]}, raising=False)

    with pytest.raises(SimulationInProductionError, match="SimulationFactory cannot run"):
        SimulationFactory.create_ornstein_uhlenbeck(DUMMY_DEVICE_ID, DUMMY_SENSOR_ID, SensorType.BME280)

@pytest.mark.parametrize("env", ["simulation", "development", "staging"])
def test_guard_allows_valid_environments(monkeypatch: pytest.MonkeyPatch, env: str):
    monkeypatch.setenv("DEPLOYMENT_ENVIRONMENT", env)
    SimulationFactory._guard()  # pyright: ignore[reportPrivateUsage]

def test_guard_uses_simulation_as_default(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DEPLOYMENT_ENVIRONMENT", raising=False)
    SimulationFactory._guard()  # pyright: ignore[reportPrivateUsage]