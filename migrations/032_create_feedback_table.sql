CREATE TABLE IF NOT EXISTS feedback (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    star_rating INTEGER CHECK (star_rating >= 1 AND star_rating <= 5),
    feedback_text TEXT,
    name VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
