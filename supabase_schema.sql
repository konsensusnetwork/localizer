-- Translation runs table for storing job information
CREATE TABLE IF NOT EXISTS translation_runs (
    id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    job_id VARCHAR(255) UNIQUE NOT NULL,
    book_path TEXT NOT NULL,
    model VARCHAR(100) NOT NULL,
    language VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    output_file TEXT,
    error TEXT,
    token_usage JSONB DEFAULT '{}',
    config JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_translation_runs_user_id ON translation_runs(user_id);
CREATE INDEX IF NOT EXISTS idx_translation_runs_job_id ON translation_runs(job_id);
CREATE INDEX IF NOT EXISTS idx_translation_runs_status ON translation_runs(status);
CREATE INDEX IF NOT EXISTS idx_translation_runs_created_at ON translation_runs(created_at DESC);

-- Row Level Security (RLS) policies
ALTER TABLE translation_runs ENABLE ROW LEVEL SECURITY;

-- Policy to allow users to read their own translation runs
CREATE POLICY "Users can read their own translation runs" ON translation_runs
    FOR SELECT USING (auth.uid()::text = user_id);

-- Policy to allow users to insert their own translation runs
CREATE POLICY "Users can insert their own translation runs" ON translation_runs
    FOR INSERT WITH CHECK (auth.uid()::text = user_id);

-- Policy to allow users to update their own translation runs
CREATE POLICY "Users can update their own translation runs" ON translation_runs
    FOR UPDATE USING (auth.uid()::text = user_id);

-- Policy to allow users to delete their own translation runs
CREATE POLICY "Users can delete their own translation runs" ON translation_runs
    FOR DELETE USING (auth.uid()::text = user_id);

-- Storage buckets for file uploads
INSERT INTO storage.buckets (id, name, public) VALUES 
    ('translation-files', 'translation-files', false),
    ('translation-logs', 'translation-logs', false)
ON CONFLICT (id) DO NOTHING;

-- Storage policies for translation files bucket
CREATE POLICY "Users can upload their own files" ON storage.objects
    FOR INSERT WITH CHECK (bucket_id = 'translation-files' AND auth.uid()::text = (storage.foldername(name))[1]);

CREATE POLICY "Users can read their own files" ON storage.objects
    FOR SELECT USING (bucket_id = 'translation-files' AND auth.uid()::text = (storage.foldername(name))[1]);

CREATE POLICY "Users can delete their own files" ON storage.objects
    FOR DELETE USING (bucket_id = 'translation-files' AND auth.uid()::text = (storage.foldername(name))[1]);

-- Storage policies for translation logs bucket
CREATE POLICY "Users can upload their own logs" ON storage.objects
    FOR INSERT WITH CHECK (bucket_id = 'translation-logs' AND auth.uid()::text = (storage.foldername(name))[1]);

CREATE POLICY "Users can read their own logs" ON storage.objects
    FOR SELECT USING (bucket_id = 'translation-logs' AND auth.uid()::text = (storage.foldername(name))[1]);

CREATE POLICY "Users can delete their own logs" ON storage.objects
    FOR DELETE USING (bucket_id = 'translation-logs' AND auth.uid()::text = (storage.foldername(name))[1]);

-- Function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update the updated_at column
CREATE TRIGGER update_translation_runs_updated_at 
    BEFORE UPDATE ON translation_runs 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();