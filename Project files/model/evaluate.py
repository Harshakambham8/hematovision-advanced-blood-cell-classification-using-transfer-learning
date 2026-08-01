import os
import logging
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support, roc_curve, auc
from tensorflow.keras.models import load_model

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def evaluate_model(model_path=Config.MODEL_PATH, test_generator=None):
    """
    Evaluate trained model performance on test dataset and print detailed evaluation report.
    """
    if not os.path.exists(model_path):
        logger.error(f"Model file not found at {model_path}")
        return None

    logger.info(f"Loading trained model from {model_path} for evaluation...")
    model = load_model(str(model_path))
    
    if test_generator is None:
        logger.warning("No test generator provided. Skipping batch evaluation.")
        return None
        
    logger.info("Evaluating model on test dataset...")
    y_true = test_generator.classes
    y_pred_probs = model.predict(test_generator)
    y_pred = np.argmax(y_pred_probs, axis=1)
    
    # Classification Report
    report = classification_report(y_true, y_pred, target_names=Config.CLASS_NAMES, output_dict=True)
    logger.info("Classification Report Generated:")
    print(classification_report(y_true, y_pred, target_names=Config.CLASS_NAMES))
    
    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plot_confusion_matrix(cm, Config.CLASS_NAMES)
    
    return {
        'classification_report': report,
        'confusion_matrix': cm.tolist()
    }

def plot_confusion_matrix(cm, class_names, output_path=Config.BASE_DIR / 'reports' / 'confusion_matrix.png'):
    """Plot and save confusion matrix heat map."""
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=class_names, yticklabels=class_names,
           title='Blood Cell Classification Confusion Matrix',
           ylabel='True Label',
           xlabel='Predicted Label')
           
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    fmt = 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
                    
    fig.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    logger.info(f"Saved Confusion Matrix graphic to {output_path}")

def plot_training_history(history, output_path=Config.BASE_DIR / 'reports' / 'training_curves.png'):
    """Plot Accuracy and Loss curves over epochs."""
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs_range = range(len(acc))

    plt.figure(figsize=(12, 5))
    
    # Accuracy Plot
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy', color='#0284c7', linewidth=2)
    plt.plot(epochs_range, val_acc, label='Validation Accuracy', color='#10b981', linewidth=2)
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')
    plt.grid(True, linestyle='--', alpha=0.5)

    # Loss Plot
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss', color='#ef4444', linewidth=2)
    plt.plot(epochs_range, val_loss, label='Validation Loss', color='#f59e0b', linewidth=2)
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.grid(True, linestyle='--', alpha=0.5)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    logger.info(f"Saved Training History curves to {output_path}")
