-------------------------------
-- TKAzotea database Data Model
-------------------------------

CREATE TABLE IF NOT EXISTS config_t
(
    -- This is the database counterpart of a configuration file
    -- All configurations are stored here
    section        TEXT,  -- Configuration section
    property       TEXT,  -- Property name
    value          TEXT,  -- Property value

    PRIMARY KEY(section, property)
);

CREATE TABLE IF NOT EXISTS log_dbase_stats_t
(
    -- This table holds stats and metadata parsed from a log file
    filepath       TEXT,      -- logfile absolute path
    lineno         TEXT,      -- line number withn the file whre the info was extracted
    tstamp         TIMESTAMP, -- Database stats timestamp
    total          INTEGER,   -- Total database writes (ok + nok) hourly statistics
    ok             INTEGER,   -- database writes ok hourly statistics
    nok            INTEGER,   -- database writes not ok hourly statistics

    PRIMARY KEY(tstamp)
);

CREATE TABLE IF NOT EXISTS dbase_intervals_t
(
    -- This table holds detected problematic intervals
   
    tstamp         TIMESTAMP, -- Interval start time
    duration       REAL,      -- Interval duration in seconds
    delta          INTEGER,   -- delta < 0: gap starts, delta = 0: gap continues:, delta > 0: gap ends

    FOREIGN KEY(tstamp)     REFERENCES log_dbase_stats_t(tstamp),
    PRIMARY KEY(tstamp)
);

