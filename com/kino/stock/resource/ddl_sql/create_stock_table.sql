CREATE TABLE t_stock (
	ts_code varchar(32) NOT NULL,
	symbol varchar(32) NOT NULL,
	name VARCHAR(64) NOT NULL,
	area varchar(32) NOT NULL,
	industry varchar(32) NOT NULL,
	market varchar(16) NOT NULL,
	list_date INT NOT NULL,
	created_time DATETIME NOT NULL,
	updated_time DATETIME NOT NULL
)
ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE UNIQUE INDEX t_stock_UNIQUE_IDX USING BTREE ON t_stock (ts_code);