# Offshore Pipeline

> An event-driven IoT data pipeline from simulated sensor readings to encrypted MQTT telemetry.

The name draws inspiration from industrial data pipelines in remote and offshore environments. *Offshore* refers to IoT devices deployed in fields, facilities, and unmanned locations, while *Pipeline* represents the event-driven flow that carries their data through the system.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![CI](https://github.com/dragomirj/offshore-pipeline/actions/workflows/kiln.yml/badge.svg)](https://github.com/dragomirj/offshore-pipeline/actions/workflows/kiln.yml)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

CI runs flake8, mypy, and pytest (with 80% coverage minimum) on Python 3.11 through 3.13, on Linux and Windows.

## Table of Contents

- [Overview](#overview)
- [Why This Project Exists](#why-this-project-exists)
- [Getting Started](#getting-started)
- [Example Payload](#example-payload)
- [Components](#components)
- [Design Decisions](#design-decisions)
- [What's Next](#whats-next)
- [License](#license)

## Overview

Offshore Pipeline is an end-to-end, event-driven IoT data pipeline. It simulates physical sensors (ADXL345, BME280, MQ7, MQ135, and SCD40), assembles their readings into structured events, and publishes encrypted telemetry over MQTT. The architecture is designed to grow toward real-time analytics with Apache Kafka and Apache Spark.

## Why This Project Exists

Real IoT deployments often take months to source, deploy, and fine-tune hardware before a
single byte reaches Apache Kafka. Most IoT demos work around this by reaching
for `random.random()`, which generates completely uncorrelated noise. That kind of data is
not useful for training ML models, does not behave meaningfully in ksqlDB alerting pipelines,
and does not resemble real sensor output in any practical sense.

This platform takes a different approach by using established stochastic processes matched to each sensor class:

- **Ornstein-Uhlenbeck (OU)** for polled sensors measuring slowly-varying environmental quantities such as temperature, humidity, and gas concentration. Values drift around realistic baselines, depend on the previous reading, and produce anomalies naturally.
- **Cox-Ingersoll-Ross (CIR)** for interrupt-driven sensors measuring signals such as vibration magnitude. It can be derived from the magnitude of three independent OU axes, remains non-negative by construction, and scales noise with the current level. Quiet periods produce less variation while energetic periods produce more.

Both processes are spike-aware: transient events such as sudden gas exposure, interference, or abnormal activity are modeled through configurable probability, magnitude, and duration parameters.

The architecture is also designed to be **hardware-ready**. Switching from simulated data to
real sensors is as simple as changing an environment variable.

## Getting Started 

**Prerequisites**: Python 3.11+. You will need an accessible MQTT broker. If you do not already have one, the included Docker Compose setup can start one locally.

### Install 

```bash
git clone https://github.com/dragomirj/offshore-pipeline.git
cd offshore-pipeline
pip install -r requirements.txt
```

### Start the MQTT broker

```bash
docker compose up -d
```

This starts a Mosquitto broker bound to `127.0.0.1:1883`. Skip this step if you are pointing at an existing broker.

### Run

```bash
python main.py
```

By default this runs in simulation mode using the `device.yaml` device profile, publishing to the local Mosquitto broker at `127.0.0.1:1883`. You should see sensor readings published every 0.5 seconds per sensor.

### Run tests

```bash
pytest
```

### Configuration

| Variable                 | Default      | Description                                                                              |
|--------------------------|--------------|------------------------------------------------------------------------------------------|
| `DEPLOYMENT_ENVIRONMENT` | `simulation` | `simulation` uses OU and CIR simulators. `production` loads hardware drivers.            |
| `PIPELINE_CIPHER_KEY`    | unset        | Hex key for AES-GCM or ChaCha20-Poly1305. Required when `pipeline.cipher` is not `none`. |

Broker settings (host, port, client ID) live in `config/mqtt.yaml`. The codec and cipher scheme live in `config/pipeline.yaml`.

### Device profile

Device and sensor configuration lives in `config/device.yaml`:

```yaml
sensors:
  - sensor_id: bme280
    sensor_type: bme280
    poll_interval_seconds: 1.0
    warmup_seconds: 30.0
    enabled: true
    alert_thresholds:
      temperature_c: 85.0
      humidity_rh: 95.0
      pressure_hpa: 1100.0
    params:
      i2c_address: 0x77
```

| Key                     | Required | Description                                                      |
|-------------------------|----------|------------------------------------------------------------------|
| `sensor_id`             | yes      | Unique identifier for the sensor within the device               |
| `sensor_type`           | yes      | One of the supported sensor type values                          |
| `poll_interval_seconds` | no       | How often the sensor is read, in seconds (default: `1.0`)        |
| `warmup_seconds`        | no       | Seconds to wait after init before reading (default: `0.0`)       |
| `enabled`               | no       | Whether the sensor is active (default: `true`)                   |
| `alert_thresholds`      | no*      | Per-channel thresholds for hardware mode. Ignored in simulation. |
| `params`                | no**     | Hardware parameters required by the sensor driver                |

\* `alert_thresholds` can be omitted in simulation mode. In hardware mode, drivers that declare required threshold channels will raise a configuration error at startup if any are missing.

\** `params` can be omitted when the sensor driver declares no required parameters. Sensors that do require parameters will raise a configuration error at startup listing the missing keys.

## Example Payload

A published event looks like this with the JSON codec and no encryption:

```json
{
    "channels": {
        "humidity_rh": {
            "alert_threshold": 62.5,
            "spiking": false
        },
        "pressure_hpa": {
            "alert_threshold": 1023,
            "spiking": false
        },
        "temperature_c": {
            "alert_threshold": 25.75,
            "spiking": false
        }
    },
    "data": {
        "humidity_rh": 55.009,
        "pressure_hpa": 1013.2,
        "temperature_c": 23.769
    },
    "device": {
        "device_id": "3bI7R4vddTIuQN5L",
        "firmware_version": "0.1.0",
        "location": {
            "lat": 44.823083,
            "lon": 20.447571
        },
        "sensor_id": "bme280"
    },
    "ingested_at": 1779911038987,
    "occurred_at": 1779911038987,
    "simulation": {
        "simulation_type": "ornstein_uhlenbeck"
    },
    "tags": [
        "offshore_pipeline",
        "additional_tag"
    ],
    "trace": {
        "event_id": "0e438a0c-6d27-4948-b574-75efe03c23a9",
        "span_id": "4b35d11b3f339051",
        "trace_id": "b0a3453831f8325c68632010f2870c92"
    }
}
```

## Components

| Component | Description |
|---|---|
| **Sensor Drivers** | Hardware interface for BME280, MQ7, MQ135, SCD40, and ADXL345. Two I/O models: polled (caller-timed, timeout-protected) and interrupt-driven (event-owned timing, bounded queue for drop tracking). Drivers are currently stubs with a well-defined interface for real I2C, SPI, and ADC implementations. |
| **OU Simulator** | Drop-in replacement for polled sensors. Runs an Ornstein-Uhlenbeck process per channel with configurable baseline, volatility, mean-reversion speed, and spike probability. Alert thresholds are embedded in the published payload. |
| **CIR Simulator** | Drop-in replacement for interrupt-driven sensors. Runs a Cox-Ingersoll-Ross process per channel, derived as the exact SDE for the magnitude of three independent OU axes. Stays non-negative by construction. Delivers readings on an exponentially distributed schedule matching hardware activity-interrupt behaviour. |
| **Event Assembler** | Aggregates multi-channel readings from a single sensor tick into one timestamped event. Attaches device ID, firmware version, physical location, and distributed trace identifiers. |
| **Event Pipeline** | Two-stage transformation: serialization then encryption. JSON for simulation, compact binary (protobuf) for production. Misconfiguration is caught at startup rather than at publish time. |
| **MQTT Client** | Async wrapper around Paho. Waits for broker acknowledgement before publishing. QoS 1 per message. |

**Simulated sensors:**

| Sensor  | Channels                                         | Interface       |
|---------|--------------------------------------------------|-----------------|
| BME280  | `temperature_c` · `humidity_rh` · `pressure_hpa` | I2C             |
| MQ7     | `co_ppm`                                         | ADC             |
| MQ135   | `co2_ppm` · `nh3_ppm`                            | ADC             |
| SCD40   | `co2_ppm` · `temperature_c` · `humidity_rh`      | I2C             |
| ADXL345 | `vibration_g`                                    | SPI / interrupt |

In hardware mode, `alert_thresholds` must include every channel key listed above for that sensor. The required keys match the channel names exactly.

## Design Decisions

**Duck typing over inheritance at the polling boundary.**
Sensors and simulators satisfy a structural interface rather than sharing a base class. The poller depends on the contract, not the hierarchy. Adding a new sensor or simulator never requires touching the other side.

**Each transport gets its own implementation.**
MQTT, Kafka, and CoAP differ at the protocol model level in ways that actually matter: publish/subscribe versus request/response versus observe. A shared transport abstraction would strip QoS semantics, retain flags, and per-publish control from MQTT without giving anything back. Each transport is added as a standalone component when needed.

**Misconfiguration is a startup error, not a runtime one.**
The pipeline validates its codec and cipher combination when it is built, not when it publishes. An insecure configuration in staging or production fails immediately. There is no path to accidentally publishing unprotected data.

**Serialization and encryption are independent stages.**
The two transformations are composed at construction time and know nothing about each other. Moving from human-readable JSON in simulation to compact encrypted binary in production is a config change.

**Warmup runs after hardware initialization, not before.**
Sensors with heater circuits need those circuits active before the stabilization window starts. Sleeping before hardware initialization wastes the entire warmup period.

## What's Next

The analytics layer is not yet built. The plan is to add an MQTT-to-Kafka bridge as the next milestone. Apache Kafka would be the entry point for everything downstream, with ksqlDB for stream alerting and Apache Spark for batch analytics. The "each transport gets its own implementation" decision exists partly because MQTT and Apache Kafka have fundamentally different semantics that a shared interface would flatten.

Hardware drivers are the other incomplete piece. The driver interface is well-defined and real I2C, SPI, and ADC implementations slot in without touching any other layer.

## License

Offshore Pipeline is licensed under the MIT License. See [LICENSE](LICENSE) for details.
