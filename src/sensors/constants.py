# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [SENSORS] Constants
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <13-Feb-2026>
# *****************************************************************************
POLLED_SENSOR_READ_TIMEOUT = 1.5  # Timeout for reading from a polled sensor (seconds)
INTERRUPT_SENSOR_MAX_QUEUE_SIZE = 64  # Maximum number of unprocessed events
SENSOR_POLLER_MAX_ERRORS = 9  # Maximum consecutive read errors before giving up
SENSOR_POLLER_BACKOFF_CAP = 30.0  # Upper bound on exponential backoff between retries (seconds)