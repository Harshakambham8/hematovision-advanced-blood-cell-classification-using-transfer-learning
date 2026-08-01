import os
import pytest
from config import Config
from services.database import init_db, save_prediction, get_prediction_by_id, delete_prediction, get_history, get_dashboard_stats

def test_database_crud(tmp_path, monkeypatch):
    test_db = tmp_path / "test_sqlite.db"
    monkeypatch.setattr(Config, "DATABASE_PATH", test_db)
    monkeypatch.setattr(Config, "DATABASE_DIR", tmp_path)
    
    init_db()
    assert test_db.exists()
    
    top_probs = {'Eosinophil': 5.0, 'Lymphocyte': 10.0, 'Monocyte': 5.0, 'Neutrophil': 80.0}
    pred_id = save_prediction(
        filename="test_file.jpg",
        filepath=str(tmp_path / "test_file.jpg"),
        original_filename="sample.jpg",
        predicted_class="Neutrophil",
        confidence=80.0,
        inference_time=25.5,
        top_probabilities=top_probs
    )
    
    assert pred_id is not None and pred_id > 0
    
    record = get_prediction_by_id(pred_id)
    assert record is not None
    assert record['predicted_class'] == "Neutrophil"
    assert record['top_probabilities']['Neutrophil'] == 80.0
    
    history = get_history()
    assert len(history) == 1
    
    stats = get_dashboard_stats()
    assert stats['total_predictions'] == 1
    assert stats['class_distribution']['Neutrophil'] == 1
    
    deleted = delete_prediction(pred_id)
    assert deleted is True
    assert get_prediction_by_id(pred_id) is None
