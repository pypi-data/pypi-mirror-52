# -*- coding: utf-8 -*-
"""Exceptions for Abfallwirtschaft Fulda."""


class AbfallwirtschaftFuldaError(Exception):
    """Generic Abfallwirtschaft Fulda exception."""

    pass


class AbfallwirtschaftFuldaConnectionError(AbfallwirtschaftFuldaError):
    """Abfallwirtschaft Fulda connection exception."""

    pass


class AbfallwirtschaftFuldaAddressError(AbfallwirtschaftFuldaError):
    """Abfallwirtschaft Fulda unknown address exception."""

    pass
