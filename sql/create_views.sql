CREATE OR REPLACE VIEW LongTermPositionView AS
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
    JOIN q ON t.Symbol = q.Symbol
  WHERE t.Quantity != 0;


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
    JOIN q ON t.Symbol = q.Symbol
  WHERE t.Quantity != 0;

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
      FROM LongTermPositionView l
        JOIN Securities s ON l.Symbol = s.Symbol
        JOIN AssetAllocationPlan a ON s.TypeId = a.TypeId
        JOIN InvestmentPlan i ON i.PlanId = a.PlanId
      GROUP BY PlanId, TypeId
    ) v;

CREATE OR REPLACE VIEW SpeculationHedgeView AS
  WITH p AS
    (
      # Positions
      SELECT
        t.Symbol,
        t.TypeId,
        SUM(t.Quantity)                             AS OpenQuantity,
        -SUM(t.PrincipalAmount) - SUM(t.Commission) AS Balance
      FROM Transactions t
      WHERE t.TypeId = 'HEDGE'
         OR t.TypeId = 'SPECULATION'
      GROUP BY 1, 2
    ), c AS
    (
      # Closed positions
      SELECT
        p.TypeId,
        SUM(Balance) AS ProfitOrLoss
      FROM p
      WHERE p.OpenQuantity = 0
      GROUP BY 1
    ), o AS
    (
      # Open positions
      SELECT
        p.TypeId,
        SUM(Balance) AS OpenPosition
      FROM p
      WHERE p.OpenQuantity != 0
      GROUP BY 1
    ), t AS
    (
      SELECT
        t.TypeId,
        ((
          SELECT SUM(MarketValue)
          FROM ShortTermPositionView
        ) + (
          SELECT SUM(MarketValue)
          FROM LongTermPositionView
        )) * 0.05 AS TotalBase,
        (
          SELECT SUM(ProfitOrLoss)
          FROM c
        ) AS TotalProfitOrLoss,
        (
          CASE WHEN t.TypeId = 'HEDGE' THEN 0.6 ELSE 0.4 END
        ) AS Percentage
      FROM TransactionTypes t
      WHERE t.TypeId = 'HEDGE'
         OR t.TypeId = 'SPECULATION'
    )
    SELECT
      t.TypeId,
      ROUND(t.TotalBase * t.Percentage, 6) AS Base,
      ROUND(COALESCE(c.ProfitOrLoss, 0), 6) AS ProfitOrLoss,
      ROUND((t.TotalBase + t.TotalProfitOrLoss) * t.Percentage, 6) AS Balance,
      ROUND(-COALESCE(o.OpenPosition, 0), 6) OpenPosition
    FROM t
    LEFT JOIN c
      ON c.TypeId = t.TypeId
    LEFT JOIN o
      ON o.TypeId = t.TypeId;
