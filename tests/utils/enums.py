# *****************************************************************************
# Copyright (C) 2026 Dragomir J. - [UTILS] Enum Utilities
# *****************************************************************************
# Licensed under the MIT License (see LICENSE file in the root directory)
# SPDX-License-Identifier: MIT
# Written by Dragomir J. <04-May-2026>
# *****************************************************************************
import inspect
import importlib
import pkgutil
from src.common.enums.base import ParsableEnum

def get_all_parsable_enums(package_name: str) -> list[type[ParsableEnum]]:
    parsable_enums: list[type[ParsableEnum]] = []
    package = importlib.import_module(package_name)

    for _, module_name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        module = importlib.import_module(module_name)
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if (issubclass(obj, ParsableEnum) and obj is not ParsableEnum):
                parsable_enums.append(obj)

    return parsable_enums