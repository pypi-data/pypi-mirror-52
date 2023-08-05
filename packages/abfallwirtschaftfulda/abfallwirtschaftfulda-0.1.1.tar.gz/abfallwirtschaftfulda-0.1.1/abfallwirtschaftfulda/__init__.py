# -*- coding: utf-8 -*-
"""Asynchronous Python client for the Abfallwirtschaft Fulda API."""

from .const import (  # noqa
    WASTE_TYPE_NON_RECYCLABLE,
    WASTE_TYPE_NON_RECYCLABLE_RED,
    WASTE_TYPE_NON_RECYCLABLE_GREEN,
    WASTE_TYPE_ORGANIC,
    WASTE_TYPE_PAPER,
    WASTE_TYPE_PLASTIC,
    # Altkleidersammlung
)
from .abfallwirtschaftfulda import (  # noqa
    AbfallwirtschaftFulda,
    AbfallwirtschaftFuldaAddressError,
    AbfallwirtschaftFuldaConnectionError,
    AbfallwirtschaftFuldaError,
)
