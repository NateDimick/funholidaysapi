SELECT holiday 
FROM holidays
WHERE month = (%s) AND day = (%s);