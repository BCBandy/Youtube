USE Stonks

SELECT	  daily.symbol
		, daily.[date] AS currentDate
		, ROUND((daily.[high] - daily.[open])/daily.[open], 2) AS gap_pct
FROM dbo.daily
WHERE daily.[open] >= 1
	AND daily.[open] < 30
	AND ((daily.[high] + daily.[low]) / 2) * daily.volume >= 8*1000000	-- dollar volume
	AND (daily.[high] - daily.[open])/daily.[open] >= .6			-- pct gain from open
ORDER BY daily.[date] DESC








