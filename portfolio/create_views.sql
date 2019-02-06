CREATE OR REPLACE VIEW LongTermInvestmentView AS
  SELECT
    t.Symbol,
    t.Quantity,
    t.Quantity * q.Close AS MarketValue,
    t.Quantity * q.Close /
    (
      SELECT SUM(t.Quantity * q.Close)
      FROM Transactions t
        JOIN
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
            GROUP BY Symbol)
        ) q ON t.Symbol = q.Symbol
      WHERE
        TypeId = 'LONG_TERM'
    )                    AS Weight
  FROM
    (
      SELECT
        Symbol,
        SUM(Quantity) AS Quantity
      FROM Transactions
      WHERE
        TypeId = 'LONG_TERM'
      GROUP BY Symbol
    ) t
    JOIN
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
        GROUP BY Symbol)
    ) q ON t.Symbol = q.Symbol;

CREATE OR REPLACE VIEW AssetAllocationView AS
  SELECT
    a.PlanId,
    s.TypeId,
    SUM(l.MarketValue)                                    CurrentValue,
    a.Weight * i.AdjustedTargetValue                      AdjustedTargetValue,
    a.Weight                                              TargetWeight,
    a.Weight * i.AdjustedTargetValue - SUM(l.MarketValue) RemainingValue
  FROM LongTermInvestmentView l
    JOIN Securities s ON l.Symbol = s.Symbol
    JOIN AssetAllocationPlan a ON s.TypeId = a.TypeId
    JOIN InvestmentPlan i ON i.PlanId = a.PlanId
  GROUP BY PlanId, TypeId;
