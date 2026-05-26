# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Configuration Loader
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <19-May-2026>
# *****************************************************************************
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import yaml
from src.common.enums.device_mode import DeviceMode

CONFIG_DIR = Path(__file__).resolve().parents[1] / "config"

class ConfigError(Exception):
    pass

def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        with open(path) as f:
            data: dict[str, Any] = yaml.safe_load(f) or {}
            return data
    except FileNotFoundError:
        raise ConfigError(f"Config file not found: {path}")

def _require(mapping: dict[str, Any], *keys: str, context: str) -> None:
    missing = [k for k in keys if mapping.get(k) is None]
    if missing:
        raise ConfigError(f"{context}: missing required field(s): {', '.join(missing)}")

@dataclass
class LocationConfig:
    lat: float
    lon: float

@dataclass
class DeviceInfo:
    id:               str
    location:         LocationConfig
    mode:             DeviceMode
    firmware_version: str
    tags:             tuple[str, ...] = field(default_factory=tuple)

@dataclass
class SensorConfig:
    sensor_id:             str
    sensor_type:           str
    poll_interval_seconds: float
    warmup_seconds:        float
    enabled:               bool
    alert_thresholds:      dict[str, float]
    params:                dict[str, Any]

@dataclass
class DeviceConfig:
    device:  DeviceInfo
    sensors: list[SensorConfig]

@dataclass
class BrokerConfig:
    host:      str
    port:      int
    client_id: str
    keepalive: int

@dataclass
class PipelineConfig:
    codec:  str
    cipher: str

@dataclass
class BaseConfig:
    pipeline: PipelineConfig

def _parse_broker(raw: dict[str, Any]) -> BrokerConfig:
    mqtt: dict[str, Any] = raw.get("mqtt") or {}
    _require(mqtt, "host", "port", "client_id", "keepalive", context="mqtt.yaml")
    return BrokerConfig(
        host=str(mqtt["host"]),
        port=int(mqtt["port"]),
        client_id=str(mqtt["client_id"]),
        keepalive=int(mqtt["keepalive"]),
    )

def _parse_pipeline(raw: dict[str, Any]) -> BaseConfig:
    pipeline: dict[str, Any] = raw.get("pipeline") or {}
    _require(pipeline, "codec", "cipher", context="pipeline.yaml")
    return BaseConfig(
        pipeline=PipelineConfig(
            codec=str(pipeline["codec"]),
            cipher=str(pipeline["cipher"]),
        )
    )

def _parse_sensor(raw: dict[str, Any], filename: str) -> SensorConfig:
    _require(raw, "sensor_id", "sensor_type", context=f"{filename} [sensor]")
    raw_thresholds: dict[str, Any] = raw.get("alert_thresholds") or {}
    return SensorConfig(
        sensor_id=str(raw["sensor_id"]),
        sensor_type=str(raw["sensor_type"]),
        poll_interval_seconds=float(raw.get("poll_interval_seconds", 1.0)),
        warmup_seconds=float(raw.get("warmup_seconds", 0.0)),
        enabled=bool(raw.get("enabled", True)),
        alert_thresholds={k: float(v) for k, v in raw_thresholds.items()},
        params=dict(raw.get("params") or {}),
    )

def _parse_device(raw: dict[str, Any], filename: str) -> DeviceConfig:
    device: dict[str, Any] = raw.get("device") or {}
    _require(device, "id", "mode", "firmware_version", context=f"{filename} [device]")

    location: dict[str, Any] = device.get("location") or {}
    _require(location, "lat", "lon", context=f"{filename} [device.location]")

    raw_sensors: list[dict[str, Any]] = raw.get("sensors") or []
    if not raw_sensors:
        raise ConfigError(f"{filename}: no sensors defined — add at least one sensor")

    ids = [str(s["sensor_id"]) for s in raw_sensors if "sensor_id" in s]
    duplicates = {sid for sid in ids if ids.count(sid) > 1}
    if duplicates:
        raise ConfigError(f"{filename}: duplicate sensor_id(s): {duplicates}")

    sensors = [_parse_sensor(s, filename) for s in raw_sensors]

    raw_tags: list[str] = device.get("tags") or []
    return DeviceConfig(
        device=DeviceInfo(
            id=str(device["id"]),
            location=LocationConfig(
                lat=float(location["lat"]),
                lon=float(location["lon"]),
            ),
            mode=DeviceMode.parse(str(device["mode"])),
            firmware_version=str(device["firmware_version"]),
            tags=tuple(raw_tags),
        ),
        sensors=sensors,
    )

def load_config(device_file: str) -> tuple[BrokerConfig, BaseConfig, DeviceConfig]:
    broker_cfg = _parse_broker(_load_yaml(CONFIG_DIR / "mqtt.yaml"))
    base_cfg   = _parse_pipeline(_load_yaml(CONFIG_DIR / "pipeline.yaml"))
    device_cfg = _parse_device(_load_yaml(CONFIG_DIR / device_file), device_file)
    return broker_cfg, base_cfg, device_cfg
