USE Stonks

-- Winners
SELECT	  daily.symbol
		, daily.[date] AS currentDate
		, ROUND((daily.[high] - daily.[open])/daily.[open], 2) AS gap_pct
		, (daily.[low] + daily.[high])/2 AS price_avg
FROM dbo.daily
JOIN dbo.daily AS daily_prev
	ON daily_prev.symbol = daily.symbol
	AND daily_prev.row_count = daily.row_count - 1
JOIN dbo.daily AS daily_prev2
	ON daily_prev2.symbol = daily.symbol
	AND daily_prev2.row_count = daily.row_count - 2
WHERE daily.[open] >= .10
	--AND daily.[open] < 30
	AND ((daily.[high] + daily.[low]) / 2) * daily.volume >= 8*1000000				-- dollar volume
	AND (
			(daily_prev2.[close] - daily_prev2.[open])/daily_prev2.[open] >= .3
			AND (daily_prev.[close] - daily_prev.[open])/daily_prev.[open] <= .6
			AND (daily.[high] - daily.[open])/daily.[open] >= .6
		)																			-- pct gain from open
ORDER BY daily.[date] DESC


-- Scan no hindsight
SELECT	  'd3surge' AS setupName
		, daily.symbol
		, daily_prev2.[date] AS startDate
		, daily.[date] AS endDate
		, NULL AS [float]
		, NULL AS sharesOutstanding
		, daily.[date] AS tradeDate
		
		--, ROUND((daily.[high] - daily.[open])/daily.[open], 2) AS gap_pct
		--, (daily.[low] + daily.[high])/2 AS price_avg
FROM dbo.daily
JOIN dbo.daily AS daily_prev
	ON daily_prev.symbol = daily.symbol
	AND daily_prev.row_count = daily.row_count - 1
JOIN dbo.daily AS daily_prev2
	ON daily_prev2.symbol = daily.symbol
	AND daily_prev2.row_count = daily.row_count - 2
WHERE daily.[open] >= .10																-- min price
	--AND daily.[open] < 30																-- max price
	AND daily.volume > 1000000															-- min volume
	and daily_prev.volume > 1000000														-- prev min volume
	AND ((daily.[high] + daily.[low]) / 2) * daily.volume >= 8*1000000					-- dollar volume
	AND (daily_prev2.[close] - daily_prev2.[open])/daily_prev2.[open] >= .3				-- prev2 pct gain
	AND CASE
			WHEN daily_prev.[open] > daily_prev.[close] 
			THEN (daily_prev.[close] - daily_prev.[open])/daily_prev.[open] --pct decrease
			ELSE (daily_prev.[open] - daily_prev.[close])/daily_prev.[close] --pct increase
		END BETWEEN -.2 and .6	-- prev pct gain range
	AND daily_prev.[high] < daily_prev2.[high]											-- d1 below d2
	AND daily.[high] > daily_prev.[close]												-- high above prev close
ORDER BY daily.[date] DESC