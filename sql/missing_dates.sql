WITH d AS
(
  SELECT
    t.Symbol,
    MIN(t.Date) FirstDate,
    IF(SUM(t.Quantity) = 0, MAX(t.Date), CURDATE()) LastDate
  FROM Transactions t
  WHERE t.TypeId = 'LONG_TERM'
  GROUP BY 1
),
qd AS
(
  SELECT
    q.Symbol,
    q.Date
  FROM d
  JOIN DailyQuote q
    ON q.Symbol = d.Symbol
    AND q.Date BETWEEN d.FirstDate AND d.LastDate
),
sd AS
(
  SELECT
    d.Symbol,
    q.Date
  FROM d
  JOIN DailyQuote q
    ON q.Symbol = 'SPY'
    AND q.Date BETWEEN d.FirstDate AND d.LastDate
)
SELECT
  sd.Symbol,
  sd.Date
FROM sd
LEFT JOIN qd
  ON sd.Symbol = qd.Symbol
  AND sd.Date = qd.Date
WHERE qd.Date IS NULL
