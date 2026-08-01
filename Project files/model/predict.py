import time
import numpy as np
import tensorflow as tf
from typing import Dict, Any, Tuple
from pathlib import Path

from config import Config
from model.preprocess import load_and_preprocess_image

def predict_single_image(model: tf.keras.Model, image_path: Path) -> Tuple[str, float, float, Dict[str, float], np.ndarray]:
    """
    Run inference on a single blood cell image.
    
    Returns:
        predicted_class (str)
        confidence (float)
        inference_time (float in ms)
        top_probabilities (dict)
        img_array (np.ndarray)
    """
    start_time = time.time()
    img_array = load_and_preprocess_image(image_path)
    
    raw_preds = model.predict(img_array, verbose=0)[0]
    inference_time = round((time.time() - start_time) * 1000, 2)
    
    class_idx = int(np.argmax(raw_preds))
    predicted_class = Config.CLASS_NAMES[class_idx]
    confidence = round(float(raw_preds[class_idx]) * 100.0, 2)
    
    top_probabilities = {
        Config.CLASS_NAMES[i]: round(float(raw_preds[i]) * 100.0, 2)
        for i in range(len(Config.CLASS_NAMES))
    }
    
    return predicted_class, confidence, inference_time, top_probabilities, img_array
