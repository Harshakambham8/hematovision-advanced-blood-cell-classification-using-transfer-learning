-- SQLite Schema for HematoVision Prediction History
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    filepath TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    predicted_class TEXT NOT NULL,
    confidence REAL NOT NULL,
    inference_time REAL NOT NULL,
    top_probabilities TEXT NOT NULL, -- JSON string
    gradcam_path TEXT,
    report_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_predictions_class ON predictions(predicted_class);
CREATE INDEX IF NOT EXISTS idx_predictions_created ON predictions(created_at);
