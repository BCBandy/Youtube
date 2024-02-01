USE [Stonks]


update dbo.daily
set daily.row_count = ROW_NUMBER() OVER(PARTITION BY symbol ORDER BY [datetime])
FROM [dbo].daily
GO

select 
	 ROW_NUMBER() OVER(PARTITION BY symbol ORDER BY [datetime]) AS symbol_count
	,daily.[symbol]
	,daily.[open]
	,daily.[high]
	,daily.[low]
	,daily.[close]
	,daily.[volume]
	,[datetime]
	,CAST(DATEADD(s, [datetime], '19700101 00:00:00:000') AT TIME ZONE 'UTC' AT TIME ZONE 'Eastern Standard Time' AS DATE) AS [datetime]
FROM [dbo].daily
