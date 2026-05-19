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
from src.simulation.simulators.cox_ingersoll_ross_simulator import CoxIngersollRossSimulator
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

def test_create_polled_returns_ou_simulator(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DEPLOYMENT_ENVIRONMENT", raising=False)
    profile = _make_profile(SensorType.BME280)
    monkeypatch.setattr(SimulationFactory, "_registry", {SensorType.BME280: [profile]}, raising=False)

    simulator = SimulationFactory.create_polled(DUMMY_DEVICE_ID, DUMMY_SENSOR_ID, SensorType.BME280)

    assert isinstance(simulator, OrnsteinUhlenbeckSimulator)

def test_create_polled_raises_when_sensor_type_not_registered(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DEPLOYMENT_ENVIRONMENT", raising=False)
    monkeypatch.setattr(SimulationFactory, "_registry", {}, raising=False)

    with pytest.raises(ValueError, match="No simulation profiles"):
        SimulationFactory.create_polled(DUMMY_DEVICE_ID, DUMMY_SENSOR_ID, SensorType.BME280)

def test_create_interrupt_returns_cir_simulator(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DEPLOYMENT_ENVIRONMENT", raising=False)
    profile = _make_profile(SensorType.ADXL345)
    monkeypatch.setattr(SimulationFactory, "_registry", {SensorType.ADXL345: [profile]}, raising=False)

    simulator = SimulationFactory.create_interrupt(DUMMY_DEVICE_ID, DUMMY_SENSOR_ID, SensorType.ADXL345)

    assert isinstance(simulator, CoxIngersollRossSimulator)

def test_create_interrupt_raises_when_sensor_type_not_registered(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DEPLOYMENT_ENVIRONMENT", raising=False)
    monkeypatch.setattr(SimulationFactory, "_registry", {}, raising=False)

    with pytest.raises(ValueError, match="No simulation profiles"):
        SimulationFactory.create_interrupt(DUMMY_DEVICE_ID, DUMMY_SENSOR_ID, SensorType.ADXL345)

@pytest.mark.parametrize("env", ["production"])
def test_factory_raises_in_disallowed_environments(monkeypatch: pytest.MonkeyPatch, env: str):
    monkeypatch.setenv("DEPLOYMENT_ENVIRONMENT", env)
    profile = _make_profile(SensorType.BME280)
    monkeypatch.setattr(SimulationFactory, "_registry", {SensorType.BME280: [profile]}, raising=False)

    with pytest.raises(SimulationInProductionError, match="SimulationFactory cannot run"):
        SimulationFactory.create_polled(DUMMY_DEVICE_ID, DUMMY_SENSOR_ID, SensorType.BME280)

@pytest.mark.parametrize("env", ["simulation", "development", "staging"])
def test_guard_allows_valid_environments(monkeypatch: pytest.MonkeyPatch, env: str):
    monkeypatch.setenv("DEPLOYMENT_ENVIRONMENT", env)
    SimulationFactory._guard()  # pyright: ignore[reportPrivateUsage]

def test_guard_uses_simulation_as_default(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DEPLOYMENT_ENVIRONMENT", raising=False)
    SimulationFactory._guard()  # pyright: ignore[reportPrivateUsage]
