CREATE TABLE IF NOT EXISTS QuandlWikiStockPrices (
  Symbol            CHAR(10)                              NOT NULL,
  Date              DATE                                  NOT NULL,
  Open              decimal(19, 6)                        NULL,
  High              decimal(19, 6)                        NULL,
  Low               decimal(19, 6)                        NULL,
  Close             decimal(19, 6)                        NULL,
  Volume            double                                NOT NULL,
  ExDividend        double                                NOT NULL,
  SplitRatio        double                                NOT NULL,
  AdjOpen           double                                NULL,
  AdjHigh           double                                NULL,
  AdjLow            double                                NULL,
  AdjClose          double                                NULL,
  AdjVolume         double                                NOT NULL,
  CreationTimestamp TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (Symbol, Date),
  KEY Date (Date)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

LOAD DATA LOCAL INFILE
  '[CSV_FILE_NAME]'
INTO TABLE QuandlWikiStockPrices
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(
  Symbol,
  Date,
  @Open,
  @High,
  @Low,
  @Close,
  Volume,
  @ExDividend,
  @SplitRatio,
  @AdjOpen,
  @AdjHigh,
  @AdjLow,
  @AdjClose,
  AdjVolume
)
SET Open     = NULLIF(@Open, ''),
  High       = NULLIF(@High, ''),
  Low        = NULLIF(@Low, ''),
  Close      = NULLIF(@Close, ''),
  ExDividend = IF(@ExDividend = '', 0.0, @ExDividend),
  SplitRatio = IF(@SplitRatio = '', 1.0, @SplitRatio),
  AdjOpen    = NULLIF(@AdjOpen, ''),
  AdjHigh    = NULLIF(@AdjHigh, ''),
  AdjLow     = NULLIF(@AdjLow, ''),
  AdjClose   = NULLIF(@AdjClose, '');
