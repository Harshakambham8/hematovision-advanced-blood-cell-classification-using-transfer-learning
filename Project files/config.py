import os
from pathlib import Path

# Base Directory of the application
BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Central configuration for HematoVision application."""
    
    BASE_DIR = BASE_DIR
    
    # Application Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'hematovision-medical-ai-secure-key-2026')
    
    # Directories
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    REPORT_FOLDER = BASE_DIR / 'reports'
    LOG_FOLDER = BASE_DIR / 'logs'
    DATABASE_DIR = BASE_DIR / 'database'
    DATABASE_PATH = DATABASE_DIR / 'sqlite.db'
    
    MODEL_DIR = BASE_DIR / 'models' / 'saved_model'
    MODEL_PATH = MODEL_DIR / 'hematovision_mobilenetv2.h5'
    
    DATASET_DIR = BASE_DIR / 'dataset'
    
    # Upload Constraints
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB Max upload size
    
    # Model Hyperparameters & Specs
    CLASS_NAMES = ['Eosinophil', 'Lymphocyte', 'Monocyte', 'Neutrophil']
    IMAGE_SIZE = (224, 224)
    INPUT_SHAPE = (224, 224, 3)
    NUM_CLASSES = 4
    BATCH_SIZE = 32
    EPOCHS = 25
    LEARNING_RATE = 1e-4
    
    # Medical Information Reference
    CELL_INFO = {
        'Neutrophil': {
            'description': 'Most abundant type of white blood cells. Plays a key role in the innate immune system by responding quickly to bacterial infection.',
            'normal_range': '40% - 60% of total WBC count',
            'associated_conditions': 'Neutrophilia (bacterial infection, inflammation), Neutropenia (bone marrow failure, severe viral infection).'
        },
        'Eosinophil': {
            'description': 'Involved in combatting multicellular parasites and certain infections. Also plays a major role in allergic reactions and asthma.',
            'normal_range': '1% - 4% of total WBC count',
            'associated_conditions': 'Eosinophilia (parasitic infections, allergic conditions, asthma, autoimmune disease).'
        },
        'Monocyte': {
            'description': 'Largest type of white blood cell. Differentiates into macrophages and dendritic cells to engulf pathogens and present antigens.',
            'normal_range': '2% - 8% of total WBC count',
            'associated_conditions': 'Monocytosis (chronic infections, inflammatory disorders, autoimmune diseases, blood disorders).'
        },
        'Lymphocyte': {
            'description': 'Includes T cells, B cells, and NK cells. Essential for adaptive immunity, antibody production, and direct cell-mediated destruction of viruses.',
            'normal_range': '20% - 40% of total WBC count',
            'associated_conditions': 'Lymphocytosis (viral infections like mononucleosis, leukemia), Lymphocytopenia (immunodeficiency, steroid therapy).'
        }
    }

    @staticmethod
    def init_app():
        """Ensure all required runtime directories exist."""
        for folder in [Config.UPLOAD_FOLDER, Config.REPORT_FOLDER, Config.LOG_FOLDER, Config.DATABASE_DIR, Config.MODEL_DIR]:
            os.makedirs(folder, exist_ok=True)
