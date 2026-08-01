# HematoVision — Production-Grade Blood Cell Classification AI Web Application

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask 2.3](https://img.shields.io/badge/Flask-2.3-green.svg)](https://flask.palletsprojects.org/)
[![TensorFlow 2.12+](https://img.shields.io/badge/TensorFlow-2.12%2B-orange.svg)](https://www.tensorflow.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**HematoVision** is an enterprise-grade medical Web AI system designed to automate white blood cell (leukocyte) classification into four distinct biological categories (**Neutrophil**, **Eosinophil**, **Monocyte**, **Lymphocyte**). Built with MobileNetV2 Transfer Learning, Explainable AI (Grad-CAM), SQLite auditing, and ReportLab PDF document compilation, HematoVision delivers clinical decision support with high performance and transparency.

---

## Key Features

- **MobileNetV2 Transfer Learning**: Deep neural network utilizing ImageNet feature extraction with a customized dense classification head.
- **Explainable AI (Grad-CAM)**: Visualizes cell activation heatmaps so hematologists can inspect exact morphology regions driving predictions.
- **Interactive Medical UI**: Glassmorphism design system, drag-and-drop file upload, live preview, dynamic confidence gauges, and Chart.js analytics.
- **Hospital PDF Diagnostic Reports**: Automatically generates downloadable clinical summary reports complete with specimen comparisons, confidence metrics, and medical disclaimers.
- **SQLite Prediction Audit Trail**: Complete historical database storing prediction metrics with search, filter, and pagination support.
- **RESTful API v1**: Complete API endpoints (`/predict`, `/history`, `/statistics`, `/health`) for seamless integration with Electronic Health Record (EHR) platforms.

---

## Project Structure

```
HematoVision/
├── app.py                   # Main Flask application entry point
├── config.py                # Centralized configuration settings
├── requirements.txt         # Python package dependencies
├── README.md                # Project documentation overview
├── .gitignore               # Ignored version control patterns
├── models/                  # Directory for saved model weights
├── uploads/                 # Uploaded specimen images and Grad-CAM overlays
├── reports/                 # Generated diagnostic PDF reports
├── logs/                    # Application system logs
├── database/
│   └── schema.sql           # SQLite database schema
├── templates/               # Jinja2 HTML templates
│   ├── base.html            # Core layout template
│   ├── index.html           # Diagnostic Studio upload page
│   ├── result.html          # Prediction analysis & Grad-CAM viewer
│   ├── dashboard.html       # Clinical analytics dashboard
│   ├── history.html         # Searchable prediction history
│   └── about.html           # Educational reference & AI architecture
├── static/                  # Web static assets
│   ├── css/
│   │   └── style.css        # Medical design system styles
│   └── js/
│       ├── main.js          # Interactive upload & validation JS
│       └── dashboard.js     # Chart.js visualization handlers
├── model/                   # ML core package
│   ├── __init__.py
│   ├── preprocess.py        # Image processing & data generators
│   ├── train.py             # MobileNetV2 training script
│   ├── evaluate.py          # Metrics, confusion matrix, ROC curves
│   ├── predict.py           # Inference execution script
│   ├── gradcam.py           # Grad-CAM heatmap generator
│   └── utils.py             # File security & path utilities
├── services/                # Business logic services
│   ├── __init__.py
│   ├── classifier.py        # Main classification pipeline manager
│   ├── report_generator.py  # ReportLab PDF report builder
│   └── database.py          # SQLite database CRUD operations
├── routes/                  # Flask Blueprint route handlers
│   ├── __init__.py
│   ├── main_routes.py       # HTML page controllers
│   ├── prediction_routes.py # Form upload & download handlers
│   └── api_routes.py        # REST API endpoints
├── docs/                    # Technical documentation
│   ├── architecture.md      # System architecture specification
│   ├── workflow.md          # Execution workflow document
│   └── api.md               # REST API specification
└── tests/                   # Automated pytest suite
    ├── test_api.py          # API route unit & integration tests
    ├── test_database.py     # SQLite CRUD operations tests
    └── test_validation.py   # File validation utility tests
```

---

## Quickstart & Setup

Follow these step-by-step instructions to set up and run the HematoVision web application on your local machine:

### 1. Prerequisites
- **Python 3.10+** installed on your system.
- `pip` package manager.

### 2. Installation & Environment Setup

```bash
# 1. Clone the repository (if not already local)
git clone https://github.com/your-org/hematovision.git
cd hematovision

# 2. Create a virtual environment (Recommended)
# Windows (PowerShell / CMD):
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux:
python3 -m venv venv
source venv/bin/activate

# 3. Install required dependencies
pip install -r requirements.txt
```

### 3. Running the Web Application

Launch the Flask development server by running:

```bash
python app.py
```

Upon starting, you will see output confirming that the database schema is initialized and the server is running:

```text
Starting HematoVision Web Application on http://127.0.0.1:5000
 * Running on http://127.0.0.1:5000
```

### 4. Accessing the Application

Open your browser and navigate to:
- **Local Application URL**: [http://127.0.0.1:5000](http://127.0.0.1:5000) or [http://localhost:5000](http://localhost:5000)
- **API Health Check**: [http://127.0.0.1:5000/api/v1/health](http://127.0.0.1:5000/api/v1/health)

---

## Model Training & Evaluation

To train or re-train the MobileNetV2 model using a custom dataset of blood cell images:

```bash
# Place dataset under dataset/train and dataset/val
python model/train.py --epochs 25 --batch_size 32
```

To evaluate trained model metrics (confusion matrix, ROC curves, classification report):

```bash
python model/evaluate.py
```

---

## Automated Testing

Run the complete test suite using `pytest`:

```bash
python -m pytest tests/ -v
```

---

## RESTful API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Service health status and ML model readiness |
| `POST` | `/api/v1/predict` | Multipart image upload for cell classification |
| `GET` | `/api/v1/history` | Retrieve searchable prediction audit records |
| `DELETE` | `/api/v1/history/<id>` | Delete a specific prediction record |
| `GET` | `/api/v1/statistics` | Retrieve aggregate metrics for analytics dashboard |

---

## License & Medical Disclaimer

This project is released under the **MIT License**.

> **Medical Disclaimer:** HematoVision is intended exclusively as an auxiliary clinical decision support tool and educational research framework. All AI-generated diagnostic outputs and Grad-CAM visual heatmaps must be evaluated and verified by a certified hematologist or medical pathologist before clinical decision-making.
