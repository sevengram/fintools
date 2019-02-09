CREATE TABLE `Accounts` (
  `AccountId`         int(11)   NOT NULL AUTO_INCREMENT,
  `Brokerage`         char(20)  NOT NULL,
  `AccountNumber`     char(30)           DEFAULT NULL,
  `Description`       char(120)          DEFAULT NULL,
  `CreationTimestamp` timestamp NOT NULL DEFAULT current_timestamp()
  ON UPDATE current_timestamp(),
  PRIMARY KEY (`AccountId`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE `SecurityTypes` (
  `TypeId`            char(30)  NOT NULL,
  `Description`       char(120)          DEFAULT NULL,
  `CreationTimestamp` timestamp NOT NULL DEFAULT current_timestamp()
  ON UPDATE current_timestamp(),
  PRIMARY KEY (`TypeId`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE `TransactionTypes` (
  `TypeId`            char(30)  NOT NULL,
  `Description`       char(120)          DEFAULT NULL,
  `CreationTimestamp` timestamp NOT NULL DEFAULT current_timestamp()
  ON UPDATE current_timestamp(),
  PRIMARY KEY (`TypeId`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE `DailyQuote` (
  `Symbol`            char(10)       NOT NULL,
  `Date`              date           NOT NULL,
  `Open`              decimal(19, 6) NOT NULL,
  `High`              decimal(19, 6) NOT NULL,
  `Low`               decimal(19, 6) NOT NULL,
  `Close`             decimal(19, 6) NOT NULL,
  `Volume`            decimal(19, 6) NOT NULL,
  `PreviousClose`     decimal(19, 6) NOT NULL,
  `Currency`          char(5)        NOT NULL DEFAULT 'USD',
  `CreationTimestamp` timestamp      NOT NULL DEFAULT current_timestamp()
  ON UPDATE current_timestamp(),
  PRIMARY KEY (`Symbol`, `Date`),
  KEY `DailyQuote_Date_IDX` (`Date`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE `InvestmentPlan` (
  `PlanId`              int(11)        NOT NULL AUTO_INCREMENT,
  `Description`         char(120)               DEFAULT NULL,
  `StartDate`           date           NOT NULL,
  `EndDate`             date           NOT NULL,
  `TypeId`              char(30)       NOT NULL,
  `TargetValue`         decimal(19, 6) NOT NULL,
  `AdjustedTargetValue` decimal(19, 6) NOT NULL,
  `Currency`            char(5)        NOT NULL DEFAULT 'USD',
  `CreationTimestamp`   timestamp      NOT NULL DEFAULT current_timestamp()
  ON UPDATE current_timestamp(),
  PRIMARY KEY (`PlanId`),
  CONSTRAINT `InvestmentPlan_TransactionTypes_FK` FOREIGN KEY
    (`TypeId`) REFERENCES `TransactionTypes` (`TypeId`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE `Securities` (
  `Symbol`            char(10)  NOT NULL,
  `Description`       char(120)          DEFAULT NULL,
  `Exchange`          char(20)  NOT NULL,
  `TypeId`            char(30)  NOT NULL,
  `CreationTimestamp` timestamp NOT NULL DEFAULT current_timestamp()
  ON UPDATE current_timestamp(),
  PRIMARY KEY (`Symbol`),
  CONSTRAINT `Securities_SecurityTypes_FK` FOREIGN KEY
    (`TypeId`) REFERENCES `SecurityTypes` (`TypeId`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE `Transactions` (
  `TransactionId`     int(11)        NOT NULL AUTO_INCREMENT,
  `Symbol`            char(10)       NOT NULL,
  `Date`              date           NOT NULL,
  `AccountId`         int(11)        NOT NULL,
  `TypeId`            char(30)       NOT NULL,
  `Quantity`          int(11)        NOT NULL,
  `Price`             decimal(13, 4) NOT NULL,
  `PrincipalAmount`   decimal(13, 4)          GENERATED ALWAYS AS (`Price` * `Quantity`) VIRTUAL,
  `Commission`        decimal(13, 4) NOT NULL DEFAULT 0,
  `Currency`          char(5)        NOT NULL DEFAULT 'USD',
  `CreationTimestamp` timestamp      NOT NULL DEFAULT current_timestamp()
  ON UPDATE current_timestamp(),
  PRIMARY KEY (`TransactionId`),
  KEY `Transactions_Symbol_IDX` (`Symbol`),
  KEY `Transactions_Date_IDX` (`Date`),
  CONSTRAINT `Transactions_Accounts_FK` FOREIGN KEY
    (`AccountId`) REFERENCES `Accounts` (`AccountId`),
  CONSTRAINT `Transactions_TransactionTypes_FK` FOREIGN KEY
    (`TypeId`) REFERENCES `TransactionTypes` (`TypeId`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE `AssetAllocationPlan` (
  `PlanId`            int(11)       NOT NULL AUTO_INCREMENT,
  `TypeId`            char(30)      NOT NULL,
  `FirstDate`         date          NOT NULL,
  `FrequencyInDays`   int(11)       NOT NULL,
  `Weight`            decimal(6, 4) NOT NULL,
  `CreationTimestamp` timestamp     NOT NULL DEFAULT current_timestamp()
  ON UPDATE current_timestamp(),
  PRIMARY KEY (`PlanId`, `TypeId`),
  CONSTRAINT `AssetAllocationPlan_InvestmentPlan_FK` FOREIGN KEY
    (`PlanId`) REFERENCES `InvestmentPlan` (`PlanId`),
  CONSTRAINT `AssetAllocationPlan_SecurityTypes_FK` FOREIGN KEY
    (`TypeId`) REFERENCES `SecurityTypes` (`TypeId`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;
