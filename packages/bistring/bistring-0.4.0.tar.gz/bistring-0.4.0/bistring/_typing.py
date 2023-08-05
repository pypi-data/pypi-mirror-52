# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.

from typing import Callable, Match, Pattern, Tuple, Union


Bounds = Tuple[int, int]

AnyBounds = Union[int, range, slice, Bounds]

Index = Union[int, slice]

Range = Union[range, slice, Bounds]

Regex = Union[str, Pattern[str]]

Replacement = Union[str, Callable[[Match[str]], str]]
