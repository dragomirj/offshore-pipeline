# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] Sensor Poller Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <29-Apr-2026>
# *****************************************************************************
import pytest
import asyncio
from unittest.mock import AsyncMock, call
from src.sensors.sensor_poller import SensorPoller

@pytest.mark.asyncio
async def test_run_happy_path_calls_callback_and_sleeps(monkeypatch: pytest.MonkeyPatch):
    readable = AsyncMock()
    readable.blocks_on_read = False
    readable.read = AsyncMock(side_effect=[[7, 7, 7], asyncio.CancelledError()])
    readable.initialize = AsyncMock()
    readable.close = AsyncMock()

    callback = AsyncMock()
    sleep = AsyncMock()
    monkeypatch.setattr(asyncio, "sleep", sleep)

    poller = SensorPoller(readable, callback, poll_interval=0.1)

    with pytest.raises(asyncio.CancelledError):
        await poller.run()

    readable.initialize.assert_awaited_once()
    callback.assert_awaited_once_with([7, 7, 7])
    sleep.assert_called_with(0.1)
    readable.close.assert_awaited_once()

@pytest.mark.asyncio
async def test_run_no_sleep_when_blocking(monkeypatch: pytest.MonkeyPatch):
    readable = AsyncMock()
    readable.blocks_on_read = True
    readable.read = AsyncMock(side_effect=[[7, 7, 7], asyncio.CancelledError()])
    readable.initialize = AsyncMock()
    readable.close = AsyncMock()

    callback = AsyncMock()
    sleep = AsyncMock()
    monkeypatch.setattr(asyncio, "sleep", sleep)

    poller = SensorPoller(readable, callback, poll_interval=0.1)

    with pytest.raises(asyncio.CancelledError):
        await poller.run()

    callback.assert_awaited_once_with([7, 7, 7])
    sleep.assert_not_called()
    readable.close.assert_awaited_once()

@pytest.mark.asyncio
async def test_run_retries_then_recovers_and_resets_error_counter(monkeypatch: pytest.MonkeyPatch):
    readable = AsyncMock()
    readable.blocks_on_read = False
    readable.read = AsyncMock(side_effect=[
        Exception("Fail_1"),
        [999],  # Success should reset error count
        Exception("Fail_2"),
        asyncio.CancelledError(),
    ])
    readable.initialize = AsyncMock()
    readable.close = AsyncMock()

    callback = AsyncMock()
    sleep = AsyncMock()
    monkeypatch.setattr(asyncio, "sleep", sleep)

    poller = SensorPoller(readable, callback, poll_interval=0.1, max_errors=3)

    with pytest.raises(asyncio.CancelledError):
        await poller.run()

    # Backoff happened after first failure
    sleep.assert_any_call(0.2)

    # Normal interval sleep after success
    sleep.assert_any_call(0.1)

    callback.assert_awaited_once_with([999])
    readable.close.assert_awaited_once()

@pytest.mark.asyncio
async def test_run_raises_after_max_errors(monkeypatch: pytest.MonkeyPatch):
    readable = AsyncMock()
    readable.blocks_on_read = False
    readable.read = AsyncMock(side_effect=[
        Exception("Fail_1"),
        Exception("Fail_2"),
        Exception("Fail_3"),
    ])
    readable.initialize = AsyncMock()
    readable.close = AsyncMock()

    callback = AsyncMock()
    sleep = AsyncMock()
    monkeypatch.setattr(asyncio, "sleep", sleep)

    poller = SensorPoller(readable, callback, poll_interval=0.1, max_errors=3)

    with pytest.raises(RuntimeError, match="failed 3 consecutive times"):
        await poller.run()

    # Exponential backoff: interval * 2**error_count
    sleep.assert_has_awaits([call(0.2), call(0.4)])
    readable.close.assert_awaited_once()
    
@pytest.mark.asyncio
async def test_error_counter_properly_resets(monkeypatch: pytest.MonkeyPatch):
    # This test proves that the reset prevets premature failure
    readable = AsyncMock()
    readable.blocks_on_read = False
    readable.read = AsyncMock(side_effect=[
        Exception(),  # Count is 1
        [999],        # Reset error count
        Exception(),  # Count is 1 again, not 2
        Exception(),  # Count is 2
        asyncio.CancelledError(),  # Should NOT hit max_errors
    ])
    readable.initialize = AsyncMock()
    readable.close = AsyncMock()

    callback = AsyncMock()
    monkeypatch.setattr(asyncio, "sleep", AsyncMock())

    poller = SensorPoller(readable, callback, poll_interval=0.1, max_errors=3)

    with pytest.raises(asyncio.CancelledError):
        await poller.run()

    callback.assert_awaited_once_with([999])
    readable.close.assert_awaited_once()

@pytest.mark.asyncio
async def test_callback_exception_is_treated_as_failure(monkeypatch: pytest.MonkeyPatch):
    readable = AsyncMock()
    readable.blocks_on_read = False
    readable.read = AsyncMock(side_effect=[
        [1],  # Callback will fail
        [2],  # Recovery
        asyncio.CancelledError(),
    ])
    readable.initialize = AsyncMock()
    readable.close = AsyncMock()

    callback = AsyncMock(side_effect=[
        Exception("callback failed"),
        None,
    ])

    sleep = AsyncMock()
    monkeypatch.setattr(asyncio, "sleep", sleep)

    poller = SensorPoller(readable, callback, poll_interval=0.1, max_errors=3)

    with pytest.raises(asyncio.CancelledError):
        await poller.run()

    # First failure should trigger backoff
    sleep.assert_any_call(0.2)

    # Second call succeeds
    callback.assert_has_awaits([call([1]), call([2])])
    readable.close.assert_awaited_once()

@pytest.mark.asyncio
async def test_cancelled_error_propagates_without_counting(monkeypatch: pytest.MonkeyPatch):
    # Ensures cancellation is not treated as a retryable failure
    readable = AsyncMock()
    readable.blocks_on_read = False
    readable.read = AsyncMock(side_effect=asyncio.CancelledError())
    readable.initialize = AsyncMock()
    readable.close = AsyncMock()

    callback = AsyncMock()
    sleep = AsyncMock()
    monkeypatch.setattr(asyncio, "sleep", sleep)

    poller = SensorPoller(readable, callback, poll_interval=0.1)

    with pytest.raises(asyncio.CancelledError):
        await poller.run()

    # No retries or sleeps should occur
    sleep.assert_not_called()
    callback.assert_not_called()
    readable.close.assert_awaited_once()

@pytest.mark.asyncio
async def test_initialize_failure_does_not_call_close(monkeypatch: pytest.MonkeyPatch):
    readable = AsyncMock()
    readable.initialize = AsyncMock(side_effect=Exception("init failed"))
    readable.close = AsyncMock()

    callback = AsyncMock()

    poller = SensorPoller(readable, callback, poll_interval=0.1)

    with pytest.raises(Exception, match="init failed"):
        await poller.run()

    readable.close.assert_not_awaited()