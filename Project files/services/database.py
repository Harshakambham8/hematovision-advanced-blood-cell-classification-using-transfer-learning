import sqlite3
import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from config import Config

logger = logging.getLogger(__name__)

def get_db_connection() -> sqlite3.Connection:
    """Create and return a database connection with dictionary row formatting."""
    conn = sqlite3.connect(str(Config.DATABASE_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Initialize the SQLite database schema if not already created."""
    Config.init_app()
    schema_file = Config.BASE_DIR / 'database' / 'schema.sql'
    if schema_file.exists():
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        conn = get_db_connection()
        conn.executescript(schema_sql)
        conn.commit()
        conn.close()
        logger.info("Database schema initialized successfully.")

def save_prediction(
    filename: str,
    filepath: str,
    original_filename: str,
    predicted_class: str,
    confidence: float,
    inference_time: float,
    top_probabilities: Dict[str, float],
    gradcam_path: Optional[str] = None,
    report_path: Optional[str] = None
) -> int:
    """Insert a new prediction record into SQLite and return its inserted ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO predictions 
        (filename, filepath, original_filename, predicted_class, confidence, inference_time, top_probabilities, gradcam_path, report_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            filename,
            filepath,
            original_filename,
            predicted_class,
            confidence,
            inference_time,
            json.dumps(top_probabilities),
            gradcam_path,
            report_path
        )
    )
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def update_report_path(pred_id: int, report_path: str) -> None:
    """Update the generated PDF report path for a specific prediction."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE predictions SET report_path = ? WHERE id = ?", (report_path, pred_id))
    conn.commit()
    conn.close()

def get_history(
    search: Optional[str] = None,
    filter_class: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """Retrieve history records with optional search and filter options."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM predictions WHERE 1=1"
    params: List[Any] = []
    
    if filter_class and filter_class in Config.CLASS_NAMES:
        query += " AND predicted_class = ?"
        params.append(filter_class)
        
    if search:
        query += " AND (original_filename LIKE ? OR predicted_class LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
        
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        item = dict(row)
        item['top_probabilities'] = json.loads(item['top_probabilities'])
        results.append(item)
    return results

def get_prediction_by_id(pred_id: int) -> Optional[Dict[str, Any]]:
    """Fetch a single prediction record by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions WHERE id = ?", (pred_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        item = dict(row)
        item['top_probabilities'] = json.loads(item['top_probabilities'])
        return item
    return None

def delete_prediction(pred_id: int) -> bool:
    """Delete a prediction record and clean up associated files."""
    record = get_prediction_by_id(pred_id)
    if not record:
        return False
        
    # Attempt cleanup of physical files
    for key in ['filepath', 'gradcam_path', 'report_path']:
        path_str = record.get(key)
        if path_str:
            p = Path(path_str)
            if p.exists():
                try:
                    p.unlink()
                except Exception as e:
                    logger.warning(f"Could not delete file {p}: {e}")
                    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions WHERE id = ?", (pred_id,))
    conn.commit()
    conn.close()
    return True

def get_dashboard_stats() -> Dict[str, Any]:
    """Calculate aggregate stats for the dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM predictions")
    total = cursor.fetchone()['total']
    
    cursor.execute("SELECT AVG(confidence) as avg_conf FROM predictions")
    avg_conf_row = cursor.fetchone()['avg_conf']
    avg_confidence = round(avg_conf_row, 2) if avg_conf_row is not None else 0.0
    
    cursor.execute("SELECT AVG(inference_time) as avg_time FROM predictions")
    avg_time_row = cursor.fetchone()['avg_time']
    avg_inference_time = round(avg_time_row, 3) if avg_time_row is not None else 0.0
    
    # Class distribution breakdown
    distribution = {c: 0 for c in Config.CLASS_NAMES}
    cursor.execute("SELECT predicted_class, COUNT(*) as cnt FROM predictions GROUP BY predicted_class")
    for r in cursor.fetchall():
        if r['predicted_class'] in distribution:
            distribution[r['predicted_class']] = r['cnt']
            
    # Recent 10 predictions
    cursor.execute("SELECT * FROM predictions ORDER BY created_at DESC LIMIT 10")
    recent_rows = cursor.fetchall()
    recent = []
    for row in recent_rows:
        item = dict(row)
        item['top_probabilities'] = json.loads(item['top_probabilities'])
        recent.append(item)
        
    conn.close()
    
    return {
        'total_predictions': total,
        'average_confidence': avg_confidence,
        'average_inference_time': avg_inference_time,
        'class_distribution': distribution,
        'recent_predictions': recent
    }
