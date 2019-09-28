sql_create_fulcrum_values_table = """CREATE TABLE IF NOT EXISTS fulcrum_values (
    id INTEGER PRIMARY KEY,
    calibration REAL NOT NULL,
    throttleLow INTEGER NOT NULL,
    throttleHigh INTEGER NOT NULL
);"""

