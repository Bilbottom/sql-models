"""Parse the UK Bank Holidays from the UK Government API."""

import json

import pandas as pd
import requests


class BankHolidays:
    def __init__(self, connect_on_init: bool = True):
        self._bank_holiday_frame = pd.DataFrame(
            columns=["division", "title", "date", "notes", "bunting"]
        )
        if connect_on_init:
            self.set_bank_holiday_frame()

    @property
    def bank_holiday_frame(self):
        return self._bank_holiday_frame.rename({"date": "full_date"}, axis="columns")

    @staticmethod
    def get_uk_bank_holidays() -> dict:
        """Return the UK bank holidays from the UK government website as a dict."""
        return json.loads(
            requests.request("GET", "https://www.gov.uk/bank-holidays.json").text
        )

    def _parse_bank_holiday_division(self, division: str) -> pd.DataFrame:
        """Parse the specified division into a pandas dataframe."""
        return pd.DataFrame.from_dict(
            self.get_uk_bank_holidays()[division]["events"]
        ).assign(division=division)

    def set_bank_holiday_frame(self) -> None:
        """Convert the UK bank holidays into a pandas dataframe."""
        self._bank_holiday_frame = pd.concat(
            [
                self.bank_holiday_frame,
                *[
                    self._parse_bank_holiday_division(div)
                    for div in self.get_uk_bank_holidays()
                ],
            ]
        )


# """
# Extract the UK Bank Holidays from the UK Government API.
#
# Some related links:
#
# - https://www.gov.uk/bank-holidays
# - https://www.gov.uk/bank-holidays.json
# """
# import datetime
# import json
#
# import requests
#
# import utils.functions
#
#
# def _get_uk_bank_holidays() -> dict:
#     """
#     Return the UK bank holidays from the UK government website as a dictionary.
#
#     This directly pings the following URL:
#
#     - https://www.gov.uk/bank-holidays.json
#     """
#     return json.loads(
#         requests.request(
#             "GET",
#             "https://www.gov.uk/bank-holidays.json"
#         ).text
#     )
#
#
# class BankHolidayHandler:
#     """
#     The UK bank holidays, as defined by the UK Government API at:
#
#     - https://www.gov.uk/bank-holidays.json
#
#     Note that this currently only keeps the bank holidays for England and Wales.
#     """
#     def __init__(self, connect_on_init: bool = False, use_datetime: bool = True):
#         """
#         Create the bank holiday handler.
#
#         :param connect_on_init: Whether to get the bank holiday information from
#          the UK Government website on instantiation. Defaults to ``False``.
#         :param use_datetime: Whether to return the dates as ``datetime.date``
#          objects rather than strings in ISO-8601 format. Defaults to ``True``.
#         """
#         self._bank_holidays: list[datetime.date] | None = None
#         self.use_datetime = use_datetime
#         if connect_on_init:
#             self.retrieve_bank_holidays()
#
#     @property
#     def bank_holidays(self) -> list[str | datetime.date]:
#         """
#         A list of bank holidays in England and Wales as ``datetime.date``
#         objects.
#         """
#         if self.use_datetime:
#             return [
#                 utils.functions.string_to_date(date_str)
#                 for date_str in self._bank_holidays
#             ]
#         else:
#             return self._bank_holidays
#
#     def retrieve_bank_holidays(self) -> None:
#         """
#         Convert the UK bank holiday JSON into a list of strings representing the
#         dates in the ISO-8601 format.
#
#         This sets the ``bank_holiday`` property.
#         """
#         self._bank_holidays = [
#             obj["date"]
#             for obj in _get_uk_bank_holidays()["england-and-wales"]["events"]
#         ]
