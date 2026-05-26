# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [TRANSPORT] MQTT Client
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <12-May-2026>
# *****************************************************************************
from __future__ import annotations
import asyncio
import logging
from dataclasses import dataclass
from typing import Any
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.properties import Properties as MQTTProperties
from paho.mqtt.reasoncodes import ReasonCode
import paho.mqtt.client as mqtt

CONNACK_TIMEOUT_SECONDS = 10.0

logger = logging.getLogger(__name__)

@dataclass
class PublishResult:
    success: bool
    error: Exception | None = None

class MQTTClient:  # pragma: no cover
    """
    Paho synchronous client wrapped in run_in_executor.
    connect() blocks until CONNACK so the first publish() never races.
    """

    def __init__(self, host: str, port: int = 1883, client_id: str = "", keepalive: int = 60):
        self._host      = host
        self._port      = port
        self._keepalive = keepalive
        self._loop: asyncio.AbstractEventLoop | None = None
        self._connected = asyncio.Event()
        self._client = mqtt.Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id=client_id,
        )
        self._client.on_connect    = self._on_connect
        self._client.on_disconnect = self._on_disconnect

    def set_credentials(self, username: str, password: str = "") -> None:
        self._client.username_pw_set(username, password)

    def set_tls(self, ca_certs: str) -> None:
        self._client.tls_set(ca_certs=ca_certs)  # pyright: ignore[reportUnknownMemberType]

    def _on_connect(
        self,
        _client: mqtt.Client,
        _userdata: Any,
        _flags: mqtt.ConnectFlags,
        reason_code: ReasonCode,
        _properties: MQTTProperties | None,
    ) -> None:
        if reason_code == 0:
            logger.info("MQTT connected to %s:%d", self._host, self._port)
            if self._loop is not None:
                # _on_connect fires on paho's thread; call_soon_threadsafe is required here
                self._loop.call_soon_threadsafe(self._connected.set)
        else:
            logger.error("MQTT connection failed reason_code=%s", reason_code)

    async def connect(self, timeout: float = CONNACK_TIMEOUT_SECONDS) -> None:
        self._loop = asyncio.get_running_loop()
        self._connected.clear()
        await self._loop.run_in_executor(
            None,
            lambda: self._client.connect(self._host, self._port, self._keepalive),
        )
        self._client.loop_start()
        try:
            await asyncio.wait_for(self._connected.wait(), timeout=timeout)
        except asyncio.TimeoutError as exc:
            self._client.loop_stop()
            raise TimeoutError(
                f"MQTT CONNACK not received within {timeout}s from {self._host}:{self._port}"
            ) from exc

    def _on_disconnect(
        self,
        _client: mqtt.Client,
        _userdata: Any,
        _flags: mqtt.DisconnectFlags,
        reason_code: ReasonCode,
        _properties: MQTTProperties | None,
    ) -> None:
        if reason_code != 0:
            logger.warning("MQTT disconnected unexpectedly reason_code=%s", reason_code)
        if self._loop is not None:
            self._loop.call_soon_threadsafe(self._connected.clear)

    @property
    def is_connected(self) -> bool:
        return self._connected.is_set()

    async def publish(self, topic: str, payload: bytes, qos: int = 1, retain: bool = False) -> PublishResult:
        if self._loop is None:
            raise RuntimeError("Not connected — call connect() first")
        if not self._connected.is_set():
            return PublishResult(success=False, error=ConnectionError("Not connected"))
        try:
            def _do_publish() -> None:
                info = self._client.publish(topic, payload, qos=qos, retain=retain)
                info.wait_for_publish(timeout=5.0)

            await self._loop.run_in_executor(None, _do_publish)
            return PublishResult(success=True)
        except Exception as e:
            logger.error("MQTT publish failed: %s", e)
            return PublishResult(success=False, error=e)

    async def disconnect(self) -> None:
        self._client.loop_stop()
        self._client.disconnect()

    async def __aenter__(self) -> MQTTClient:
        await self.connect()
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.disconnect()
