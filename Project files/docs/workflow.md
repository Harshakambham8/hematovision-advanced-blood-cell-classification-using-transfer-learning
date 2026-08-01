# HematoVision End-to-End Execution Workflow

## 1. Image Ingestion & Security Validation
- User submits a microscopic image via drag-and-drop web form or REST API (`POST /api/v1/predict`).
- `model/utils.py` sanitizes filename using `secure_filename()` and prepends a UUID prefix to eliminate path traversal vulnerabilities.
- Format is checked against `ALLOWED_EXTENSIONS` (`png`, `jpg`, `jpeg`, `bmp`, `tiff`).
- File size is checked against the 16MB ceiling in `config.py`.

## 2. Preprocessing & Model Inference
- Image is loaded, converted to RGB, and resized to `(224, 224)`.
- Pixel intensities are normalized to `[0, 1]` float range.
- `services/classifier.py` invokes the pre-loaded MobileNetV2 TensorFlow model.
- Model evaluates softmax output probabilities across 4 classes: `Neutrophil`, `Eosinophil`, `Monocyte`, `Lymphocyte`.

## 3. Explainable AI (Grad-CAM)
- `model/gradcam.py` computes loss gradients with respect to the target class on the final conv layer (`Conv_1` or equivalent).
- A 2D activation heatmap is scaled to full image dimensions and colored with `cv2.COLORMAP_JET`.
- The heatmap is blended with the original specimen image at $\alpha = 0.5$ transparency and saved to disk.

## 4. History Storage & PDF Compilation
- Prediction metadata (filename, predicted class, confidence %, inference latency, probability dict, paths) are inserted into SQLite (`database/sqlite.db`).
- `services/report_generator.py` compiles a PDF report featuring clinical headers, specimen comparison, and probability distribution table.

## 5. UI Rendering
- `templates/result.html` displays the confidence meter, side-by-side salience overlay, and Chart.js probability chart.
