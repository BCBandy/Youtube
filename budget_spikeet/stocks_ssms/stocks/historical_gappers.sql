USE Stonks

SELECT	  daily.symbol
		, prev_day.[date] AS prevDate
		, daily.[date] AS currentDate
		, next_day.[date] AS nextDate
		, (daily.[open] - prev_day.[low])/prev_day.[low] AS gap_pct
FROM dbo.daily AS daily
JOIN dbo.daily AS prev_day2
	ON prev_day2.symbol = daily.symbol
	AND prev_day2.row_count = daily.row_count - 2
JOIN dbo.daily AS prev_day
	ON prev_day.symbol = daily.symbol
	AND prev_day.row_count = daily.row_count - 1
JOIN dbo.daily AS next_day
	ON next_day.symbol = daily.symbol
	AND next_day.row_count = daily.row_count + 1
WHERE daily.[open] >= 1
	AND daily.[open] < 30
	AND ((daily.[high] + daily.[low]) / 2) * daily.volume >= 8*1000000	-- dollar volume
	AND DATEDIFF(DAY,prev_day.[date], next_day.[date]) < 30				-- filter out long halts
	--AND (daily.[high] - prev_day.[low])/prev_day.[low] > .5			-- hod from prev close
	AND (daily.[open] - prev_day.[close])/prev_day.[close] >= .3		-- pct open from prev low
ORDER BY prev_day.[date] DESC
, (daily.[high] - prev_day.[low])/daily.[high] DESC




