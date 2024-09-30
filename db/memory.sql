-- Drop the table if it already exists
DROP TABLE IF EXISTS interactions;

-- Create the interactions table for storing queries and results
CREATE TABLE interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_query TEXT NOT NULL,
    sql_query TEXT NOT NULL,
    result JSON NOT NULL
);
