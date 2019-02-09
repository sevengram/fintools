CREATE OR REPLACE VIEW LongTermInvestmentView AS
  WITH t AS
  (
      SELECT
        Symbol,
        SUM(Quantity) AS Quantity
      FROM Transactions
      WHERE
        TypeId = 'LONG_TERM'
      GROUP BY Symbol
  ), q AS
  (
      SELECT
        Symbol,
        Close
      FROM DailyQuote
      WHERE (Symbol, Date) IN (
        SELECT
          Symbol,
          MAX(Date)
        FROM DailyQuote
        GROUP BY Symbol
      )
  )
  SELECT
    t.Symbol,
    t.Quantity                             AS Quantity,
    q.Close                                AS CurrentPrice,
    t.Quantity * q.Close                   AS MarketValue,
    ROUND(t.Quantity * q.Close / (
      SELECT SUM(t.Quantity * q.Close)
      FROM t
        JOIN q ON t.Symbol = q.Symbol), 4) AS Weight
  FROM t
    JOIN q ON t.Symbol = q.Symbol;


CREATE OR REPLACE VIEW ShortTermPositionView AS
  WITH t AS
  (
      SELECT
        Symbol,
        SUM(Quantity) AS Quantity
      FROM Transactions
      WHERE
        TypeId = 'SHORT_TERM'
      GROUP BY Symbol
  ), q AS
  (
      SELECT
        Symbol,
        Close
      FROM DailyQuote
      WHERE (Symbol, Date) IN (
        SELECT
          Symbol,
          MAX(Date)
        FROM DailyQuote
        GROUP BY Symbol
      )
  )
  SELECT
    t.Symbol,
    t.Quantity           AS Quantity,
    q.Close              AS CurrentPrice,
    t.Quantity * q.Close AS MarketValue
  FROM t
    JOIN q ON t.Symbol = q.Symbol;

CREATE OR REPLACE VIEW AssetAllocationView AS
  SELECT
    PlanId,
    TypeId,
    CurrentValue,
    ROUND(AdjustedTargetValue, 6)                                    AS AdjustedTargetValue,
    TargetWeight,
    ROUND(AdjustedTargetValue - CurrentValue, 6)                     AS RemainingValue,
    RemainingCycles,
    ROUND((AdjustedTargetValue - CurrentValue) / RemainingCycles, 6) AS NextCycleValue
  FROM
    (
      SELECT
        a.PlanId,
        s.TypeId,
        SUM(l.MarketValue)                                               CurrentValue,
        a.Weight * i.AdjustedTargetValue                                 AdjustedTargetValue,
        a.Weight                                                         TargetWeight,
        FLOOR(
            DATEDIFF(
                i.EndDate, a.FirstDate) / a.FrequencyInDays) -
        FLOOR(
            DATEDIFF(
                SUBDATE(CURDATE(), 1), a.FirstDate) / a.FrequencyInDays) RemainingCycles
      FROM LongTermInvestmentView l
        JOIN Securities s ON l.Symbol = s.Symbol
        JOIN AssetAllocationPlan a ON s.TypeId = a.TypeId
        JOIN InvestmentPlan i ON i.PlanId = a.PlanId
      GROUP BY PlanId, TypeId) v;
