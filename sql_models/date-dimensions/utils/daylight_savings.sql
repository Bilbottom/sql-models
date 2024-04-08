
SELECT
    year_number,
    MAX(IIF(month_number = 3,  full_date, '1900-01-01') || ' 01:00:00') AS dst_start_time_utc,
    MAX(IIF(month_number = 10, full_date, '1900-01-01') || ' 01:00:00') AS dst_end_time_utc
FROM calendar
WHERE week_day_number = 6  /* Sunday = 6, Monday = 0 */
GROUP BY year_number
ORDER BY year_number
;
