# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SIMULATION] Simulation Factory
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <30-Apr-2026>
# *****************************************************************************
from __future__ import annotations
import os
from src.common.enums.deployment_environment import DeploymentEnvironment
from src.common.enums.sensor_type import SensorType
from src.common.models.channel_profile import ChannelProfile
from src.simulation.simulators.ornstein_uhlenbeck_simulator import OrnsteinUhlenbeckSimulator
from src.simulation.simulators.constant_simulator import ConstantSimulator
from src.simulation.registry import SIMULATION_REGISTRY

class SimulationInProductionError(Exception):
    """Raised when simulation is attempted in a non-simulation environment."""
    pass

class SimulationFactory:
    _registry: dict[SensorType, list[ChannelProfile]] = dict(SIMULATION_REGISTRY)

    @staticmethod
    def _guard() -> None:
        env = DeploymentEnvironment.parse(os.getenv("DEPLOYMENT_ENVIRONMENT", "simulation"))
        if not env.supports_simulation():
            raise SimulationInProductionError(
                "SimulationFactory cannot run in the production environment. "
                "Simulated data must never enter a production pipeline. "
                "Set the deployment environment to 'simulation', 'development', or 'staging' to use simulators."
            )

    @classmethod
    def create_ornstein_uhlenbeck(cls, device_id: str, sensor_id: str, sensor_type: SensorType) -> OrnsteinUhlenbeckSimulator:
        """Creates an Ornstein-Uhlenbeck simulator for the specified sensor type, using predefined channel profiles."""
        cls._guard()
        profiles = cls._registry.get(sensor_type)
        if not profiles:
            raise ValueError(f"No simulation profiles for '{sensor_type.value}'.")
        return OrnsteinUhlenbeckSimulator(device_id, sensor_id, profiles)

    @classmethod
    def create_constant(cls, device_id: str, sensor_id: str, sensor_type: SensorType) -> ConstantSimulator:
        """Creates a Constant simulator for the specified sensor type, using predefined channel profiles."""
        cls._guard()
        profiles = cls._registry.get(sensor_type)
        if not profiles:
            raise ValueError(f"No simulation profiles for '{sensor_type.value}'.")
        return ConstantSimulator(device_id, sensor_id, profiles)