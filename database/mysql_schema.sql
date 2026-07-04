-- Zoho Catalyst MySQL Schema
-- Converted from original PostgreSQL blueprint

CREATE TABLE districts (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE stations (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    district_id VARCHAR(36),
    location POINT SRID 4326,
    FOREIGN KEY (district_id) REFERENCES districts(id)
);

CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    badge_number VARCHAR(20) UNIQUE NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    role VARCHAR(50) NOT NULL,
    rank VARCHAR(50),
    station_id VARCHAR(36),
    district_id VARCHAR(36),
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    FOREIGN KEY (station_id) REFERENCES stations(id),
    FOREIGN KEY (district_id) REFERENCES districts(id)
);

CREATE TABLE cases (
    id VARCHAR(36) PRIMARY KEY,
    case_number VARCHAR(50) UNIQUE NOT NULL,
    case_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    station_id VARCHAR(36),
    assigned_officer_id VARCHAR(36),
    incident_date DATE,
    incident_location POINT SRID 4326,
    incident_address TEXT,
    narrative TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (station_id) REFERENCES stations(id),
    FOREIGN KEY (assigned_officer_id) REFERENCES users(id)
);

CREATE INDEX idx_cases_station ON cases(station_id);
CREATE INDEX idx_cases_type_status ON cases(case_type, status);
-- MySQL spatial index requires SPATIAL INDEX and table engine to be InnoDB (or MyISAM). Note: Column must be NOT NULL for SPATIAL INDEX.
-- We skip explicit SPATIAL INDEX here for broader compatibility, or add it later if incident_location is NOT NULL.

CREATE TABLE entities (
    id VARCHAR(36) PRIMARY KEY,
    canonical_name VARCHAR(300) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    neo4j_node_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE entity_aliases (
    id VARCHAR(36) PRIMARY KEY,
    entity_id VARCHAR(36),
    alias_text VARCHAR(300) NOT NULL,
    script VARCHAR(20),
    source_case_id VARCHAR(36),
    confidence DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entity_id) REFERENCES entities(id) ON DELETE CASCADE,
    FOREIGN KEY (source_case_id) REFERENCES cases(id)
);

CREATE INDEX idx_aliases_entity ON entity_aliases(entity_id);
-- FULLTEXT search in MySQL replaces PostgreSQL's to_tsvector
ALTER TABLE entity_aliases ADD FULLTEXT(alias_text);

CREATE TABLE case_entity_links (
    case_id VARCHAR(36),
    entity_id VARCHAR(36),
    role VARCHAR(100),
    confidence DECIMAL(3,2),
    PRIMARY KEY (case_id, entity_id, role),
    FOREIGN KEY (case_id) REFERENCES cases(id),
    FOREIGN KEY (entity_id) REFERENCES entities(id)
);

CREATE TABLE conversations (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    case_id VARCHAR(36) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (case_id) REFERENCES cases(id)
);
