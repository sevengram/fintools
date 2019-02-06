CREATE TABLE Accounts (
  AccountId         int(11)   NOT NULL AUTO_INCREMENT,
  Brokerage         char(20)  NOT NULL,
  AccountNumber     char(30)           DEFAULT NULL,
  Description       char(120)          DEFAULT NULL,
  CreationTimestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (AccountId)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

CREATE TABLE SecurityTypes (
  TypeId            char(30)  NOT NULL,
  Description       char(120)          DEFAULT NULL,
  CreationTimestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (TypeId)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

CREATE TABLE Securities (
  Symbol            char(10)  NOT NULL,
  Description       char(120)          DEFAULT NULL,
  Exchange          char(20)  NOT NULL,
  TypeId            char(30)  NOT NULL,
  CreationTimestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (Symbol),
  CONSTRAINT Securities_TypeIdFK FOREIGN KEY (TypeId) REFERENCES SecurityTypes (TypeId)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

CREATE TABLE TransactionTypes (
  TypeId            char(30)  NOT NULL,
  Description       char(120)          DEFAULT NULL,
  CreationTimestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (TypeId)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

CREATE TABLE Transactions (
  TransactionId     int(11)        NOT NULL AUTO_INCREMENT,
  Symbol            char(10)       NOT NULL,
  Date              date           NOT NULL,
  AccountId         int(11)        NOT NULL,
  TypeId            char(30)       NOT NULL,
  Quantity          int(11)        NOT NULL,
  Price             decimal(13, 4) NOT NULL,
  Commission        decimal(13, 4) NOT NULL DEFAULT '0.0000',
  Currency          char(5)        NOT NULL DEFAULT 'USD',
  CreationTimestamp timestamp      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (TransactionId),
  KEY SymbolKey (Symbol),
  KEY DateKey (Date),
  KEY Transactions_TypeIdFK (TypeId),
  KEY Transactions_AccountIdFK (AccountId),
  CONSTRAINT Transactions_AccountIdFK FOREIGN KEY (AccountId) REFERENCES Accounts (
    AccountId),
  CONSTRAINT Transactions_TypeIdFK FOREIGN KEY (TypeId) REFERENCES TransactionTypes (TypeId)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

CREATE TABLE DailyQuote (
  Symbol            char(10)       NOT NULL,
  Date              date           NOT NULL,
  Open              decimal(19, 6) NOT NULL,
  High              decimal(19, 6) NOT NULL,
  Low               decimal(19, 6) NOT NULL,
  Close             decimal(19, 6) NOT NULL,
  Volume            decimal(19, 6) NOT NULL,
  PreviousClose     decimal(19, 6) NOT NULL,
  Currency          char(5)        NOT NULL DEFAULT 'USD',
  CreationTimestamp timestamp      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (Symbol, Date),
  KEY Date (Date)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

CREATE TABLE InvestmentPlan (
  PlanId              int(11)        NOT NULL AUTO_INCREMENT,
  Description         char(120)               DEFAULT NULL,
  StartDate           date           NOT NULL,
  EndDate             date           NOT NULL,
  TypeId              char(30)       NOT NULL,
  TargetValue         decimal(19, 6) NOT NULL,
  AdjustedTargetValue decimal(19, 6) NOT NULL,
  Currency            char(5)        NOT NULL DEFAULT 'USD',
  CreationTimestamp   timestamp      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (PlanId),
  CONSTRAINT InvestmentPlan_TypeIdFK FOREIGN KEY (TypeId) REFERENCES TransactionTypes (TypeId)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

CREATE TABLE InvestmentPlan (
  PlanId              int(11)        NOT NULL AUTO_INCREMENT,
  Description         char(120)               DEFAULT NULL,
  StartDate           date           NOT NULL,
  EndDate             date           NOT NULL,
  TypeId              char(30)       NOT NULL,
  TargetValue         decimal(19, 6) NOT NULL,
  AdjustedTargetValue decimal(19, 6) NOT NULL,
  Currency            char(5)        NOT NULL DEFAULT 'USD',
  CreationTimestamp   timestamp      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (PlanId),
  CONSTRAINT InvestmentPlan_TypeIdFK FOREIGN KEY (TypeId) REFERENCES TransactionTypes (TypeId)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

CREATE TABLE AssetAllocation (
  PlanId            int(11)       NOT NULL,
  TypeId            char(30)      NOT NULL,
  Weight            decimal(6, 4) NOT NULL,
  CreationTimestamp timestamp     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (PlanId, TypeId),
  CONSTRAINT AssetAllocation_PlanIdFK FOREIGN KEY (PlanId) REFERENCES InvestmentPlan (PlanId),
  CONSTRAINT AssetAllocation_TypeIdFK FOREIGN KEY (TypeId) REFERENCES SecurityTypes (TypeId)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;


