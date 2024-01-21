import sys
sys.path.append('../../')  # Add the parent directory to the sys.path
from historical.example import alpaca as ha
import db_utils
from datetime import datetime
import pandas as pd

print(ha.get_daily('TSLA'))

daily_df = ha.get_daily('TSLA')

params = [
    ['TSLA', *row] 
    for row in daily_df[['open', 'high', 'low', 'close', 'volume', 'datetime']].values
    ]

sql = f'''MERGE INTO dbo.daily AS target
USING (VALUES (?,?,?,?,?,?,?)) AS source (symbol, [open], [high], [low], [close], volume, [datetime])
ON target.symbol = source.symbol AND target.[datetime] = source.[datetime]
WHEN MATCHED AND target.[open] <> source.[open] THEN
UPDATE SET
target.[open] = source.[open],
target.[high] = source.[high],
target.[low] = source.[low],
target.[close] = source.[close],
target.volume = source.volume,
target.[datetime] = source.[datetime]
WHEN NOT MATCHED THEN
INSERT (symbol, [open], [high], low, [close], volume, [datetime])
VALUES (source.symbol, source.[open], source.[high], source.[low], source.[close], source.volume, source.[datetime]);'''
                #print(sql)

db_utils.run_sql_many(sql, params)

sql2 = '''
begin 
if not exists(select * from dbo.nasdaq_screener_All where Symbol = ?) 
insert into dbo.nasdaq_screener_All (Symbol, Name, Exchange) 
select ?, ?, ?
end'''