# HematoVision REST API Documentation

Base URL: `/api/v1`

---

### 1. Health Check
* **Endpoint:** `GET /health`
* **Description:** Check server status and model load state.
* **Response (200 OK):**
```json
{
  "app_name": "HematoVision AI Medical Server",
  "model_status": "loaded",
  "status": "healthy",
  "version": "2.0.0"
}
```

---

### 2. Classify Blood Cell Image
* **Endpoint:** `POST /predict`
* **Content-Type:** `multipart/form-data`
* **Payload:** `file` (image file)
* **Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "filename": "a1b2c3d4_sample.jpg",
    "original_filename": "sample.jpg",
    "predicted_class": "Neutrophil",
    "confidence": 96.42,
    "inference_time": 42.15,
    "top_probabilities": {
      "Eosinophil": 1.20,
      "Lymphocyte": 1.10,
      "Monocyte": 1.28,
      "Neutrophil": 96.42
    },
    "image_url": "/uploads/a1b2c3d4_sample.jpg",
    "gradcam_url": "/uploads/gradcam_a1b2c3d4_sample.jpg",
    "report_url": "/reports/report_pred_1.pdf"
  }
}
```

---

### 3. Get Prediction History
* **Endpoint:** `GET /history`
* **Query Parameters:**
  - `search` (optional string)
  - `class` (optional string: `Neutrophil`, `Eosinophil`, `Monocyte`, `Lymphocyte`)
  - `limit` (default: 50)
  - `offset` (default: 0)
* **Response (200 OK):**
```json
{
  "status": "success",
  "count": 1,
  "data": [ ... ]
}
```

---

### 4. Delete Prediction Record
* **Endpoint:** `DELETE /history/<id>`
* **Response (200 OK):**
```json
{
  "status": "success",
  "message": "Prediction ID 1 deleted successfully."
}
```

---

### 5. Get Clinical Statistics
* **Endpoint:** `GET /statistics`
* **Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "average_confidence": 94.15,
    "average_inference_time": 38.4,
    "class_distribution": {
      "Eosinophil": 5,
      "Lymphocyte": 12,
      "Monocyte": 8,
      "Neutrophil": 25
    },
    "total_predictions": 50
  }
}
```
