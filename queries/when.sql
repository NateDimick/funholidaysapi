SELECT month, day, holiday
FROM holidays
WHERE LOWER(holiday) LIKE LOWER(%s)