DROP TABLE `StockPriceVolume`;

CREATE TABLE IF NOT EXISTS `StockPriceVolume` (
  `Symbol`            CHAR(10)                              NOT NULL,
  `Date`              DATE                                  NOT NULL,
  `Open`              DOUBLE                                NULL,
  `High`              DOUBLE                                NULL,
  `Low`               DOUBLE                                NULL,
  `Close`             DOUBLE                                NULL,
  `Volume`            DOUBLE                                NOT NULL,
  `ExDividend`        DOUBLE                                NOT NULL,
  `SplitRatio`        DOUBLE                                NOT NULL,
  `AdjOpen`           DOUBLE                                NULL,
  `AdjHigh`           DOUBLE                                NULL,
  `AdjLow`            DOUBLE                                NULL,
  `AdjClose`          DOUBLE                                NULL,
  `AdjVolume`         DOUBLE                                NOT NULL,
  `CreationTimestamp` TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Symbol`, `Date`),
  KEY `Date` (`Date`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

#LOAD DATA INFILE '/var/lib/mysql-files/stock_price_volume_20180316.csv'
LOAD DATA LOCAL INFILE '/home/jfan/Downloads/WIKI_PRICES_212b326a081eacca455e13140d7bb9db.csv'
INTO TABLE `StockPriceVolume`
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(@Symbol,
 `Date`,
 @Open,
 @High,
 @Low,
 @Close,
 `Volume`,
 @ExDividend,
 @SplitRatio,
 @AdjOpen,
 @AdjHigh,
 @AdjLow,
 @AdjClose,
 `AdjVolume`)
SET
  `Symbol`     = UPPER(@Symbol),
  `Open`       = NULLIF(@Open, ''),
  `High`       = NULLIF(@High, ''),
  `Low`        = NULLIF(@Low, ''),
  `Close`      = NULLIF(@Close, ''),
  `ExDividend` = IF(@ExDividend = '', 0.0, @ExDividend),
  `SplitRatio` = IF(@SplitRatio = '', 1.0, @SplitRatio),
  `AdjOpen`    = NULLIF(@AdjOpen, ''),
  `AdjHigh`    = NULLIF(@AdjHigh, ''),
  `AdjLow`     = NULLIF(@AdjLow, ''),
  `AdjClose`   = NULLIF(@AdjClose, '');