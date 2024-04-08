import calendar
import re

import pandas as pd


class DateDimension:
    def __init__(self, start: str, end: str):
        def is_string_iso_8601(string: str) -> bool:
            return re.match(r"^\d{4}-\d{2}-\d{2}$", string=string) is not None

        if not is_string_iso_8601(start):
            raise ValueError(
                f"`start` must be a valid date in ISO-8601 format. {start} is invalid"
            )
        if not is_string_iso_8601(end):
            raise ValueError(
                f"`end` must be a valid date in ISO-8601 format. {end} is invalid"
            )

        self.date_index: pd.DatetimeIndex = self._create_datetime_index(start, end)
        self.date_frame: pd.DataFrame = self.date_index.to_frame(
            name="full_date", index=True
        )
        self.add_columns_to_date_frame()

    @staticmethod
    def _create_datetime_index(start: str, end: str) -> pd.DatetimeIndex:
        """https://stackoverflow.com/a/23190286/8213085"""
        return pd.date_range(start=start, end=end)

    def _add_datetime_attributes(self) -> None:
        """https://pandas.pydata.org/docs/reference/api/pandas.DatetimeIndex.html"""
        attributes = {
            "year": "year_number",
            "quarter": "quarter_number",
            "month": "month_number",
            "day": "day_number",
            "day_of_year": "year_day_number",
            "day_of_week": "week_day_number",  # Monday = 0, Sunday = 6
            "is_month_start": "is_month_start",
            "is_month_end": "is_month_end",
            "is_quarter_start": "is_quarter_start",
            "is_quarter_end": "is_quarter_end",
            "is_year_start": "is_year_start",
            "is_year_end": "is_year_end",
            "is_leap_year": "is_leap_year",
        }
        for key, value in attributes.items():
            self.date_frame.loc[:, value] = getattr(self.date_index, key)

        self.date_frame.loc[:, "julian_date"] = self.date_index.to_julian_date()

    def _add_names_and_numbers(self) -> None:
        # sourcery skip: replace-apply-with-numpy-operation
        self.date_frame.loc[:, "day_name"] = self.date_frame.loc[
            :, "week_day_number"
        ].apply(lambda n: calendar.day_name[n])

        self.date_frame.loc[:, "day_name_abbr"] = self.date_frame.loc[
            :, "week_day_number"
        ].apply(lambda n: calendar.day_abbr[n])

        self.date_frame.loc[:, "month_name"] = self.date_frame.loc[
            :, "month_number"
        ].apply(lambda n: calendar.month_name[n])

        self.date_frame.loc[:, "month_name_abbr"] = self.date_frame.loc[
            :, "month_number"
        ].apply(lambda n: calendar.month_abbr[n])

        self.date_frame.loc[:, "is_day_weekday"] = self.date_frame.loc[
            :, "day_name_abbr"
        ].apply(lambda s: s not in ["Sun", "Sat"])

        # noinspection PyUnresolvedReferences
        self.date_frame.loc[:, "week_number_iso"] = self.date_frame.index.isocalendar()[
            "week"
        ]

        # To match `dbo.date_dimension_table` -- use '%W' for Monday start of week
        self.date_frame.loc[:, "week_number"] = self.date_frame.loc[
            :, "full_date"
        ].apply(lambda d: 1 + int(d.strftime("%U")))

    def _add_period_ids(self) -> None:
        self.date_frame.loc[:, "period_id"] = (
            ""
            + self.date_frame["year_number"].astype(str).str.zfill(4)
            + self.date_frame["month_number"].astype(str).str.zfill(2)
            + self.date_frame["day_number"].astype(str).str.zfill(2)
        ).astype(int)
        self.date_frame.loc[:, "month_year"] = (
            ""
            + self.date_frame["year_number"].astype(str).str.zfill(4)
            + self.date_frame["month_number"].astype(str).str.zfill(2)
        ).astype(int)
        self.date_frame.loc[:, "ordinal_date"] = (
            ""
            + self.date_frame["year_number"].astype(str).str.zfill(4)
            + self.date_frame["year_day_number"].astype(str).str.zfill(3)
        ).astype(int)

    def _add_last_weekdays_of_month(self) -> None:
        last_weekdays_per_month = (
            self.date_frame[self.date_frame["is_day_weekday"]]
            .groupby("month_year")["full_date"]
            .max()
            .to_list()
        )
        self.date_frame.loc[:, "is_last_weekday_of_month"] = self.date_frame.loc[
            :, "full_date"
        ].apply(lambda d: d in last_weekdays_per_month)

    def _add_accounting_periods(self) -> None:
        for i in range(1, 25):
            self.date_frame[f"date_plus_{i:02d}_months"] = self.date_frame[
                "full_date"
            ] + pd.DateOffset(months=i)
            self.date_frame[f"date_minus_{i:02d}_months"] = self.date_frame[
                "full_date"
            ] + pd.DateOffset(months=-i)

    def _reorder_columns(self) -> None:
        # print(list(self.date_frame.columns))
        self.date_frame = self.date_frame[
            [
                "full_date",
                "period_id",
                "julian_date",
                "ordinal_date",
                "month_year",
                "year_number",
                "quarter_number",
                "month_number",
                "week_number_iso",
                "week_number",
                "day_number",
                "year_day_number",
                "week_day_number",
                "day_name",
                "day_name_abbr",
                "month_name",
                "month_name_abbr",
                "is_month_start",
                "is_month_end",
                "is_quarter_start",
                "is_quarter_end",
                "is_year_start",
                "is_year_end",
                "is_leap_year",
                "is_day_weekday",
                "is_last_weekday_of_month",
                "date_plus_01_months",
                "date_plus_02_months",
                "date_plus_03_months",
                "date_plus_04_months",
                "date_plus_05_months",
                "date_plus_06_months",
                "date_plus_07_months",
                "date_plus_08_months",
                "date_plus_09_months",
                "date_plus_10_months",
                "date_plus_11_months",
                "date_plus_12_months",
                "date_plus_13_months",
                "date_plus_14_months",
                "date_plus_15_months",
                "date_plus_16_months",
                "date_plus_17_months",
                "date_plus_18_months",
                "date_plus_19_months",
                "date_plus_20_months",
                "date_plus_21_months",
                "date_plus_22_months",
                "date_plus_23_months",
                "date_plus_24_months",
                "date_minus_01_months",
                "date_minus_02_months",
                "date_minus_03_months",
                "date_minus_04_months",
                "date_minus_05_months",
                "date_minus_06_months",
                "date_minus_07_months",
                "date_minus_08_months",
                "date_minus_09_months",
                "date_minus_10_months",
                "date_minus_11_months",
                "date_minus_12_months",
                "date_minus_13_months",
                "date_minus_14_months",
                "date_minus_15_months",
                "date_minus_16_months",
                "date_minus_17_months",
                "date_minus_18_months",
                "date_minus_19_months",
                "date_minus_20_months",
                "date_minus_21_months",
                "date_minus_22_months",
                "date_minus_23_months",
                "date_minus_24_months",
            ]
        ]

    def add_columns_to_date_frame(self) -> None:
        self._add_datetime_attributes()
        self._add_names_and_numbers()
        self._add_period_ids()
        self._add_last_weekdays_of_month()
        self._add_accounting_periods()
        self._reorder_columns()
