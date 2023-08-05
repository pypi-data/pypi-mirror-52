# -*- coding: utf-8 -*-
"""Abfallwirtschaft Fulda constants."""

API_HOST = "www.abfallwirtschaft-landkreis-fulda.de"
API_BASE_URI = "/app/ical.php"

WASTE_TYPE_NON_RECYCLABLE = "Non-recyclable"
WASTE_TYPE_NON_RECYCLABLE_RED = "Non-recyclable red"
WASTE_TYPE_NON_RECYCLABLE_GREEN = "Non-recyclable green"
WASTE_TYPE_ORGANIC = "Organic"
WASTE_TYPE_PAPER = "Paper"
WASTE_TYPE_PLASTIC = "Plastic"
WASTE_TYPE_RECYCLING_CENTER_OPENED = "Recycling Center"


API_TO_WASTE_TYPE = {
    "Bio-Tonne": WASTE_TYPE_ORGANIC,
    "Gelbe Tonne": WASTE_TYPE_PLASTIC,
    "Papier-Tonne": WASTE_TYPE_PAPER,
    "Restmüll 14-tägig": WASTE_TYPE_NON_RECYCLABLE,
    "Restmüll rot": WASTE_TYPE_NON_RECYCLABLE_RED,
    "Restmüll grün": WASTE_TYPE_NON_RECYCLABLE_GREEN,
    "Abgabetermin Wertstoffhof": WASTE_TYPE_RECYCLING_CENTER_OPENED,
}
