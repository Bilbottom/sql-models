
PRAGMA FOREIGN_KEYS = OFF;

DROP TABLE IF EXISTS calendar;
DROP TABLE IF EXISTS bank_holidays;


------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------

PRAGMA FOREIGN_KEYS = ON;

CREATE TABLE calendar(
    full_date                DATE NOT NULL PRIMARY KEY,
    period_id                INTEGER NOT NULL UNIQUE,
    julian_date              REAL NOT NULL UNIQUE,
    ordinal_date             INTEGER NOT NULL UNIQUE,
    month_year               INTEGER NOT NULL,
    year_number              INTEGER NOT NULL,
    quarter_number           INTEGER NOT NULL,
    month_number             INTEGER NOT NULL,
    week_number_iso          INTEGER NOT NULL,
    week_number              INTEGER NOT NULL,
    day_number               INTEGER NOT NULL,
    year_day_number          INTEGER NOT NULL,
    week_day_number          INTEGER NOT NULL,
    day_name                 TEXT NOT NULL,
    day_name_abbr            TEXT NOT NULL,
    month_name               TEXT NOT NULL,
    month_name_abbr          TEXT NOT NULL,
    is_month_start           BOOLEAN NOT NULL,
    is_month_end             BOOLEAN NOT NULL,
    is_quarter_start         BOOLEAN NOT NULL,
    is_quarter_end           BOOLEAN NOT NULL,
    is_year_start            BOOLEAN NOT NULL,
    is_year_end              BOOLEAN NOT NULL,
    is_leap_year             BOOLEAN NOT NULL,
    is_day_weekday           BOOLEAN NOT NULL,
    is_last_weekday_of_month BOOLEAN NOT NULL,
    date_plus_01_months      DATETIME NOT NULL,
    date_plus_02_months      DATETIME NOT NULL,
    date_plus_03_months      DATETIME NOT NULL,
    date_plus_04_months      DATETIME NOT NULL,
    date_plus_05_months      DATETIME NOT NULL,
    date_plus_06_months      DATETIME NOT NULL,
    date_plus_07_months      DATETIME NOT NULL,
    date_plus_08_months      DATETIME NOT NULL,
    date_plus_09_months      DATETIME NOT NULL,
    date_plus_10_months      DATETIME NOT NULL,
    date_plus_11_months      DATETIME NOT NULL,
    date_plus_12_months      DATETIME NOT NULL,
    date_plus_13_months      DATETIME NOT NULL,
    date_plus_14_months      DATETIME NOT NULL,
    date_plus_15_months      DATETIME NOT NULL,
    date_plus_16_months      DATETIME NOT NULL,
    date_plus_17_months      DATETIME NOT NULL,
    date_plus_18_months      DATETIME NOT NULL,
    date_plus_19_months      DATETIME NOT NULL,
    date_plus_20_months      DATETIME NOT NULL,
    date_plus_21_months      DATETIME NOT NULL,
    date_plus_22_months      DATETIME NOT NULL,
    date_plus_23_months      DATETIME NOT NULL,
    date_plus_24_months      DATETIME NOT NULL,
    date_minus_01_months     DATETIME NOT NULL,
    date_minus_02_months     DATETIME NOT NULL,
    date_minus_03_months     DATETIME NOT NULL,
    date_minus_04_months     DATETIME NOT NULL,
    date_minus_05_months     DATETIME NOT NULL,
    date_minus_06_months     DATETIME NOT NULL,
    date_minus_07_months     DATETIME NOT NULL,
    date_minus_08_months     DATETIME NOT NULL,
    date_minus_09_months     DATETIME NOT NULL,
    date_minus_10_months     DATETIME NOT NULL,
    date_minus_11_months     DATETIME NOT NULL,
    date_minus_12_months     DATETIME NOT NULL,
    date_minus_13_months     DATETIME NOT NULL,
    date_minus_14_months     DATETIME NOT NULL,
    date_minus_15_months     DATETIME NOT NULL,
    date_minus_16_months     DATETIME NOT NULL,
    date_minus_17_months     DATETIME NOT NULL,
    date_minus_18_months     DATETIME NOT NULL,
    date_minus_19_months     DATETIME NOT NULL,
    date_minus_20_months     DATETIME NOT NULL,
    date_minus_21_months     DATETIME NOT NULL,
    date_minus_22_months     DATETIME NOT NULL,
    date_minus_23_months     DATETIME NOT NULL,
    date_minus_24_months     DATETIME NOT NULL
);


CREATE TABLE bank_holidays(
    division  TEXT NOT NULL,
    title     TEXT NOT NULL,
    full_date TEXT NOT NULL REFERENCES calendar(full_date),
    notes     TEXT NOT NULL,
    bunting   BOOLEAN NOT NULL,
    PRIMARY KEY(division, full_date)
);


CREATE TABLE daylight_savings(
    region             TEXT NOT NULL,  /* This may change -- but for now, will stick to the UK/EU */
    year_number        INTEGER NOT NULL REFERENCES calendar(year_number),
    dst_start_time_utc DATETIME NOT NULL,
    dst_end_time_utc   DATETIME NOT NULL,
    PRIMARY KEY(region, year_number)
);
/*
In the UK:
* DST starts on the last Sunday in March at 01:00 UTC
* DST end on the last Sunday in October at 01:00 UTC
Between these dates and times, the time in the UK is UTC +1 hour

For example, in 2022:
* When local standard time was about to reach
    Sunday, 27 March 2022, 01:00:00 clocks were turned forward 1 hour to
    Sunday, 27 March 2022, 02:00:00 local daylight time instead.
* When local daylight time was about to reach
    Sunday, 30 October 2022, 02:00:00 clocks were turned backward 1 hour to
    Sunday, 30 October 2022, 01:00:00 local standard time instead.

Sources:
    * https://en.wikipedia.org/wiki/Daylight_saving_time_by_country
    * https://www.timeanddate.com/time/change/uk
*/
