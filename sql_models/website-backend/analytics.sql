/*
Consider a user to be "active" on a given day if they were logged in on
that day.

Logins expire after 24 hours, and only manual logouts are recorded in
the events table. Another login within 24 hours of a previous login
keeps the user logged in.
*/

with recursive

-- events(event_id, user_id, event_datetime, event_type) as (
--     values
--         (1,  1, '2024-01-01 01:03:00'::timestamp, 'login'),
--         (2,  1, '2024-01-03 01:02:00'::timestamp, 'login'),
--         (3,  1, '2024-01-04 01:01:00'::timestamp, 'login'),
--         (4,  1, '2024-01-05 01:00:00'::timestamp, 'logout'),
--         (5,  1, '2024-01-06 01:05:00'::timestamp, 'logout'),
--         (6,  1, '2024-01-06 01:06:00'::timestamp, 'logout'),
--         (7,  2, '2024-01-07 01:07:00'::timestamp, 'login'),
--         (8,  2, '2024-01-08 01:08:00'::timestamp, 'login'),
--         (9,  2, '2024-01-09 01:09:00'::timestamp, 'login'),
--         (10, 2, '2024-01-09 01:10:00'::timestamp, 'logout'),
--         (11, 2, '2024-01-10 01:11:00'::timestamp, 'logout'),
--         (12, 2, '2024-01-11 01:12:00'::timestamp, 'logout')
-- ),

event_groups as (
    select
        event_id,
        user_id,
        event_type,
        event_datetime as login_datetime,
        (0
            + row_number() over (partition by user_id             order by event_datetime)
            - row_number() over (partition by user_id, event_type order by event_datetime)
        ) as event_group,
        coalesce(
            (
                select min(event_datetime)
                from events as innr
                where 1=1
                    and events.event_type = 'login'
                    and innr.event_type = 'logout'
                    and events.user_id = innr.user_id
                    and events.event_datetime < innr.event_datetime
                    and innr.event_datetime <= events.event_datetime + interval '1 day'
            ),
            events.event_datetime + interval '1 day'
        ) as logout_datetime
    from events
),

sessions as (
    select
        user_id,
        min(login_datetime)::date as login_date,
        max(logout_datetime)::date as logout_date
    from event_groups
    where event_type = 'login'
    group by user_id, event_group
),

dates(active_date) as (
    select unnest(generate_series(
        (select min(login_date) from sessions),
        (select max(logout_date) from sessions),
        interval '1 day'
    ))
),

activity(user_id, active_date, is_active) as (
    select
        users.user_id,
        dates.active_date::date as active_date,
        if(sessions.user_id is null, 0, 1) as is_active,
        row_number() over (
            partition by users.user_id
            order by dates.active_date desc
        ) as step
    from (select distinct user_id from sessions) as users
        cross join dates
        left join sessions
            on  users.user_id = sessions.user_id
            and dates.active_date between sessions.login_date
                                     and sessions.logout_date
)

select
    user_id,
    max(active_date) as last_update,
    sum(is_active * power(2, step - 1)) as activity_history,
    to_binary(activity_history::ubigint) as activity_history_binary
from activity
group by user_id
order by user_id
;
