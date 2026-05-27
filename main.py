# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - Offshore Pipeline
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <07-May-2026>
# *****************************************************************************
import asyncio
import logging
import os
import sys
from dotenv import load_dotenv

# paho-mqtt socket integration requires add_reader/add_writer, which on Windows
# are only available on SelectorEventLoop (ProactorEventLoop is the default).
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from src.common.enums.deployment_environment import DeploymentEnvironment as Environment
from src.common.enums.device_mode import DeviceMode
from src.common.enums.sensor_mode import SensorMode
from src.common.enums.sensor_type import SensorType
from src.common.models.sensor_event import Location
from src.common.interfaces.readable import Readable
from src.common.models.sensor_reading import SensorReading
from src.config import ConfigError, DeviceConfig, SensorConfig, load_config
from src.events.assembler import AssemblerConfig, EventAssembler
from src.codec.event_codec import EventCodecFactory
from src.sensors.factory import SensorConfigError, SensorFactory
from src.sensors.sensor_poller import SensorPoller
from src.simulation.factory import SimulationFactory, SimulationInProductionError
from src.transport.mqtt_client import MQTTClient

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)-30s - %(message)s",
)
logger = logging.getLogger(__name__)

def build_readables(device_cfg: DeviceConfig, env: Environment) -> list[tuple[Readable, SensorConfig]]:
    device_id = device_cfg.device.id

    if device_cfg.device.mode == DeviceMode.SIMULATION and not env.supports_simulation():
        raise SimulationInProductionError(
            f"Device mode is 'simulation' but environment is '{env.value}'. "
            "Set device.mode to 'hardware' or use a simulation-permitted environment."
        )

    readables: list[tuple[Readable, SensorConfig]] = []

    for cfg in device_cfg.sensors:
        if not cfg.enabled:
            logger.info("Skipping disabled sensor: %s", cfg.sensor_id)
            continue

        sensor_type = SensorType.parse(cfg.sensor_type)
        if device_cfg.device.mode == DeviceMode.HARDWARE:
            readable = SensorFactory.create(device_id, cfg)
        elif sensor_type.mode == SensorMode.INTERRUPT:
            readable = SimulationFactory.create_interrupt(
                device_id=device_id,
                sensor_id=cfg.sensor_id,
                sensor_type=sensor_type,
                mean_interval_seconds=cfg.poll_interval_seconds,
            )
        else:
            readable = SimulationFactory.create_polled(
                device_id=device_id,
                sensor_id=cfg.sensor_id,
                sensor_type=sensor_type,
            )

        logger.info("Ready - sensor_id=%-10s  type=%s", cfg.sensor_id, cfg.sensor_type)
        readables.append((readable, cfg))

    return readables


async def main() -> None:
    env = Environment(os.getenv("DEPLOYMENT_ENVIRONMENT", "simulation").lower())
    device_file = "device.yaml"

    logger.info("=" * 60)
    logger.info("Offshore Pipeline starting")
    logger.info("Environment : %s", env.value.upper())
    logger.info("Device file : %s", device_file)
    logger.info("=" * 60)

    try:
        broker_cfg, base_cfg, device_cfg = load_config(device_file)
    except ConfigError as e:
        logger.error("Startup failed - %s", e)
        return

    codec = EventCodecFactory.create(
        codec=base_cfg.pipeline.codec,
        cipher=base_cfg.pipeline.cipher,
    )

    logger.info("Codec: encoding=%s, cipher=%s", codec.encoding, codec.cipher_scheme)

    mqtt_client = MQTTClient(
        host=broker_cfg.host,
        port=broker_cfg.port,
        client_id=broker_cfg.client_id,
        keepalive=broker_cfg.keepalive,
    )

    await mqtt_client.connect()

    assembler = EventAssembler(
        AssemblerConfig(
            firmware_version=device_cfg.device.firmware_version,
            location=Location(
                lat=device_cfg.device.location.lat,
                lon=device_cfg.device.location.lon,
            ),
            tags=device_cfg.device.tags,
        )
    )

    try:
        readables_with_cfg = build_readables(device_cfg, env)
    except (SensorConfigError, SimulationInProductionError, ValueError) as e:
        logger.error("Startup failed - %s", e)
        await mqtt_client.disconnect()
        return

    logger.info("Initialised %d sensor(s) for device '%s'", len(readables_with_cfg), device_cfg.device.id)
    logger.info("-" * 60)
    logger.info("Starting %d poller(s) - press Ctrl+C to stop", len(readables_with_cfg))
    logger.info("-" * 60)

    publish_counts: dict[str, int] = {}
    publish_errors: dict[str, int] = {}

    async def on_readings(readings: list[SensorReading], sensor_type: SensorType, sensor_id: str) -> None:
        event   = assembler.assemble(readings)
        payload = codec.encode(event)
        topic   = f"{device_cfg.device.id}/{sensor_type.value}"
        result  = await mqtt_client.publish(topic, payload, qos=1)

        publish_counts[sensor_id] = publish_counts.get(sensor_id, 0) + 1
        count = publish_counts[sensor_id]

        if result.success:
            channel_summary = "  ".join(f"{ch}={val:.1f}" for ch, val in event.data.items())
            logger.info("PUBLISHED #%-5d topic=%-25s | %s", count, topic, channel_summary)
        else:
            publish_errors[sensor_id] = publish_errors.get(sensor_id, 0) + 1
            logger.error(
                "PUBLISH FAILED #%d  sensor=%s  error=%s  (total errors: %d)",
                count, sensor_id, result.error, publish_errors[sensor_id],
            )

    pollers = [
        SensorPoller(
            readable=readable,
            callback=lambda r, st=SensorType.parse(cfg.sensor_type), sid=cfg.sensor_id: on_readings(r, st, sid),
            poll_interval_seconds=cfg.poll_interval_seconds,
        )
        for readable, cfg in readables_with_cfg
    ]

    try:
        async with asyncio.TaskGroup() as tg:
            for p in pollers:
                tg.create_task(p.run())
    except* asyncio.CancelledError:
        logger.info("Shutdown requested")
    finally:
        total  = sum(publish_counts.values())
        errors = sum(publish_errors.values())
        logger.info("-" * 60)
        logger.info("Shutdown - published: %d  errors: %d", total, errors)
        await mqtt_client.disconnect()
        logger.info("MQTT disconnected")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
