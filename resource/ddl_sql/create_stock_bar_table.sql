CREATE TABLE kino_stock.t_stock_bar (
  ts_code varchar(32) NOT NULL,
  trade_date INT NOT NULL,
  `open` DECIMAL(9, 4) NOT NULL,
  high DECIMAL(9, 4) NOT NULL,
  low DECIMAL(9, 4) NOT NULL,
  `close` DECIMAL(9, 4) NOT NULL,
  pre_close DECIMAL(9, 4) DEFAULT NULL,
  `change` DECIMAL(3, 3) DEFAULT NULL,
  pct_chg DECIMAL(3, 3) DEFAULT NULL,
  vol DECIMAL(19, 4) NOT NULL,
  amount DECIMAL(19, 4) NOT NULL,
  freq varchar(8) NOT NULL,
  adj varchar(8) NOT NULL,
  adj_factor DECIMAL(9, 4) DEFAULT NULL
)
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE UNIQUE INDEX t_stock_bar_UNIQUE_IDX USING BTREE ON kino_stock.t_stock_bar (ts_code, trade_date, freq, adj);