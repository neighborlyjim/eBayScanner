-- Initialize eBay Scanner Database
-- This script runs when the PostgreSQL container starts for the first time

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant all privileges to the ebay_user
GRANT ALL PRIVILEGES ON DATABASE ebay_scanner TO ebay_user;

-- Create initial schema (Alembic will handle the rest)
-- Tables will be created by running 'alembic upgrade head'
