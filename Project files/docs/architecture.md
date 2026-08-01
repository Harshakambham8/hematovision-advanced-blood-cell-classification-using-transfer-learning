# HematoVision Technical Architecture

## Overview

HematoVision is built on a modular, decoupled Flask blueprint architecture supported by MobileNetV2 Deep Learning, Grad-CAM Explainable AI, SQLite persistence, and ReportLab PDF document compilation.

```
                  +-----------------------------------+
                  |        Client Interface           |
                  | Bootstrap 5 / JS / Chart.js UI    |
                  +-----------------+-----------------+
                                    | HTTP / REST API
                                    v
                  +-----------------+-----------------+
                  |      Flask Web Layer (app.py)     |
                  |  Blueprints: main, predict, api   |
                  +--------+----------------+---------+
                           |                |
             +-------------+                +-------------+
             v                                            v
+------------+------------+                  +------------+------------+
|   Inference Service     |                  |     Database Service      |
| (services/classifier.py)|                  |   (services/database.py) |
+------------+------------+                  +------------+------------+
             |                                            |
             +------------+                  +------------+
                          |                  |
                          v                  v
              +-----------+------------------+-----------+
              |     MobileNetV2 / Grad-CAM / SQLite      |
              +------------------------------------------+
```

## Core Modules

1. **Config Layer (`config.py`)**: Centralized application configuration, file upload constraints, model hyperparameters, and cell reference details.
2. **Model Package (`model/`)**:
   - `preprocess.py`: Image normalization, scaling, data augmentation pipelines.
   - `train.py`: MobileNetV2 transfer learning setup, callbacks, early stopping.
   - `evaluate.py`: Confusion matrix, metrics calculation, and performance plotting.
   - `gradcam.py`: Explainable AI salience map generation with OpenCV overlay.
3. **Service Layer (`services/`)**:
   - `classifier.py`: End-to-end classification manager and fallback handling.
   - `report_generator.py`: Hospital-formatted diagnostic PDF generator using ReportLab.
   - `database.py`: Thread-safe SQLite operations for prediction auditing.
4. **Blueprint Routes (`routes/`)**:
   - `main_routes.py`: Dynamic view controllers.
   - `prediction_routes.py`: Upload handlers and report delivery.
   - `api_routes.py`: RESTful JSON endpoints.
