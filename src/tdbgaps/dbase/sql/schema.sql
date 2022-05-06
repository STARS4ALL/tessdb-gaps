-------------------------------
-- TKAzotea database Data Model
-------------------------------

-- This is the database counterpart of a configuration file
-- All configurations are stored here
CREATE TABLE IF NOT EXISTS config_t
(
    section        TEXT,  -- Configuration section
    property       TEXT,  -- Property name
    value          TEXT,  -- Property value

    PRIMARY KEY(section, property)
);

CREATE TABLE IF NOT EXISTS log_dbase_stats_t
(
    filepath       TEXT,      -- logfile absolute path
    lineno         TEXT,      -- line number withn the file whre the info was extracted
    tstamp         TIMESTAMP, -- Database stats timestamp
    total          INTEGER,   -- Total database writes (ok + nok) hourly statistics
    ok             INTEGER,   -- database writes ok hourly statistics
    nok            INTEGER,   -- database writes not ok hourly statistics

    PRIMARY KEY(tstamp)
);

