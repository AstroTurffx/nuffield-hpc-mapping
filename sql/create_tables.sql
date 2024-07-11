CREATE TABLE IF NOT EXISTS sites (
    site_id INTEGER PRIMARY KEY,
    website TEXT,
    name TEXT NOT NULL,
    segment TEXT,
    city TEXT NOT NULL,
    country TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS hpcs (
    system_id INTEGER PRIMARY KEY,
    site_id INTEGER NOT NULL,
    name TEXT,
    top500_rank INT,
    manufacturer TEXT,

    total_cores INTEGER,
    total_nodes INTEGER,
    processor_name TEXT NOT NULL,
    interconnect TEXT NOT NULL,

    installation_year INTEGER,
    os TEXT NOT NULL,
    r_max FLOAT,
    r_peak FLOAT,
    n_max INTEGER,

    website TEXT,
    system_tier INTEGER,
    system_status TEXT,    
    additional_info TEXT,
    FOREIGN KEY(site_id) REFERENCES sites(site_id)
);

CREATE TABLE IF NOT EXISTS node_details (
    system_id INTEGER NOT NULL,
    number INTEGER,
    processor_name TEXT,
    node_cores INTEGER,
    accelerator TEXT,
    memory INTEGER,
    FOREIGN KEY(system_id) REFERENCES hpcs(system_id)
);