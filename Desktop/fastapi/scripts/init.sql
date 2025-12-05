-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create a sample table with a vector column
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536) -- Example vector dimension
);