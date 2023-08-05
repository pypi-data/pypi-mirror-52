# -*- coding: utf-8 -*-
"""Asynchronous Python client for the Abfallwirtschaft Fulda API."""
import asyncio
import json
import socket
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

import arrow

import aiohttp
import async_timeout
from yarl import URL
import lxml.html
from ics import Calendar

from .__version__ import __version__
from .const import (
    API_BASE_URI,
    API_HOST,
    API_TO_WASTE_TYPE,
    WASTE_TYPE_NON_RECYCLABLE,
    WASTE_TYPE_NON_RECYCLABLE_RED,
    WASTE_TYPE_NON_RECYCLABLE_GREEN,
    WASTE_TYPE_ORGANIC,
    WASTE_TYPE_PAPER,
    WASTE_TYPE_PLASTIC,
    WASTE_TYPE_RECYCLING_CENTER_OPENED,
)
from .exceptions import (
    AbfallwirtschaftFuldaAddressError,
    AbfallwirtschaftFuldaConnectionError,
    AbfallwirtschaftFuldaError,
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("awf.log")
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


class AbfallwirtschaftFulda:
    """Main class for handling connections with Abfallwirtschaft Fulda."""

    def __init__(
        self,
        district_id: int,
        town_id: int,
        loop=None,
        request_timeout: int = 10,
        session=None,
        user_agent: str = None,
    ):
        """Initialize connection with Abfallwirtschaft Fulda."""
        self._loop = loop
        self._session = session
        self._close_session = False

        self.district_id = district_id
        self.town_id = town_id

        self.request_timeout = request_timeout
        self.user_agent = user_agent

        self._pickup = {}  # type: Dict[str, datetime]

        if self._loop is None:
            self._loop = asyncio.get_event_loop()

        if self._session is None:
            self._session = aiohttp.ClientSession(loop=self._loop)
            self._close_session = True

        if self.user_agent is None:
            self.user_agent = "AbfallwirtschaftFulda/{}".format(__version__)

    async def _request_ical(self, ical_url):
        """Handle a request to Abfallwirtschaft Fulda."""
        url = URL.build(scheme="https", host=API_HOST, port=443, path=ical_url)

        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json, text/plain, */*",
        }

        try:
            with async_timeout.timeout(self.request_timeout):
                response = await self._session.request(
                    "GET", url, headers=headers, ssl=True
                )
        except asyncio.TimeoutError as exception:
            raise AbfallwirtschaftFuldaConnectionError(
                "Timeout occurred while connecting to Abfallwirtschaft Fulda API."
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise AbfallwirtschaftFuldaConnectionError(
                "Error occurred while communicating with Abfallwirtschaft Fulda."
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if (response.status // 100) in [4, 5]:
            contents = await response.read()
            response.close()

            if content_type == "application/json":
                raise AbfallwirtschaftFuldaError(
                    response.status, json.loads(contents.decode("utf8"))
                )
            raise AbfallwirtschaftFuldaError(
                response.status, {"message": contents.decode("utf8")}
            )

        if "application/json" in response.headers["Content-Type"]:
            return await response.json()
        return await response.text()

    async def _request(self, data=None):
        """Handle a request to Abfallwirtschaft Fulda."""
        url = URL.build(scheme="https", host=API_HOST, port=443, path=API_BASE_URI)

        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json, text/plain, */*",
        }

        try:
            with async_timeout.timeout(self.request_timeout):
                response = await self._session.request(
                    "POST", url, data=data, headers=headers, ssl=True
                )
        except asyncio.TimeoutError as exception:
            raise AbfallwirtschaftFuldaConnectionError(
                "Timeout occurred while connecting to Abfallwirtschaft Fulda Page."
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise AbfallwirtschaftFuldaConnectionError(
                "Error occurred while communicating with Abfallwirtschaft Fulda."
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if (response.status // 100) in [4, 5]:
            contents = await response.read()
            response.close()

            if content_type == "application/json":
                raise AbfallwirtschaftFuldaError(
                    response.status, json.loads(contents.decode("utf8"))
                )
            raise AbfallwirtschaftFuldaError(
                response.status, {"message": contents.decode("utf8")}
            )

        return await response.text()

    async def update(self) -> None:
        """Fetch data from Abfallwirtschaft Fulda."""
        response = await self._request(
            data={
                "Abfuhrbezirk": self.district_id,
                "Ortschaft": self.town_id,
                "DatumVon": datetime.today().strftime("01.01.%Y"),
                "DatumBis": datetime.today().strftime("31.12.%Y"),
                "alle_abfallfraktionen": 1,
                "weiter": "%3E+%3E+weiter",
                "nummer_strasse": "",
                "sql_zusatz": "",
                "a_jahr": 2019,
                "e_jahr": 2019,
                "a_id_anfang": 2440,
                "id_ende": 2556,
                "id_ende_begin": 2556,
                "Uhrzeit_Beginn": 6,
                "Uhrzeit_Ende": 17,
                "alarm_iCal": 1440,
                "status_iCal": 1,
            }
        )

        if "Ihre Suche ergab kein Ergbnis" in response:
            raise AbfallwirtschaftFuldaAddressError(
                {"message": "Ihre Suche ergab kein Ergbnis"}
            )

        html = lxml.html.fromstring(response)
        ical_url = html.xpath('//a[@class="ical"]/@href')[0]
        response = await self._request_ical(ical_url=ical_url)
        cal = Calendar(response)

        found = {
            WASTE_TYPE_NON_RECYCLABLE: False,
            WASTE_TYPE_NON_RECYCLABLE_RED: False,
            WASTE_TYPE_NON_RECYCLABLE_GREEN: False,
            WASTE_TYPE_ORGANIC: False,
            WASTE_TYPE_PAPER: False,
            WASTE_TYPE_PLASTIC: False,
            WASTE_TYPE_RECYCLING_CENTER_OPENED: False,
        }
        yesterday = arrow.get(datetime.today() - timedelta(days=1))
        events_after = list(cal.timeline.start_after(yesterday))

        for event in events_after:
            waste_type_text = "{}".format(event.name.split(" am ")[0])
            waste_type = API_TO_WASTE_TYPE.get(waste_type_text)

            if waste_type is None:
                continue

            if found.get(waste_type) is False:
                pickup_date = None
                pickup_date = event.begin.datetime
                self._pickup.update({waste_type: pickup_date})
                found.update({waste_type: True})

        # logger.debug(self._pickup)

    async def next_pickup(self, waste_type: str) -> Optional[datetime]:
        """Return date of next pickup of the requested waste type."""
        return self._pickup.get(waste_type)

    async def close(self) -> None:
        """Close open client session."""
        if self._close_session:
            await self._session.close()

    async def __aenter__(self) -> "AbfallwirtschaftFulda":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()
