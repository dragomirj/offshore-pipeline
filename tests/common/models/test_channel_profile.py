# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [COMMON] Channel Profile Model Tests
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <18-May-2026>
# *****************************************************************************
from tests.utils.sensors import create_dummy_profile

PROFILE_MEAN = 1.0
PROFILE_STD  = 0.4

def test_alert_threshold_defaults_to_mean_plus_2_5_std_dev():
    profile = create_dummy_profile(mean=PROFILE_MEAN, std_dev=PROFILE_STD)
    assert profile.alert_threshold == PROFILE_MEAN + 2.5 * PROFILE_STD

def test_alert_threshold_explicit_value_is_preserved():
    assert create_dummy_profile(alert_threshold=3.5).alert_threshold == 3.5
