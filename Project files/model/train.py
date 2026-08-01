import os
import argparse
import logging
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

from config import Config
from model.preprocess import get_data_generators

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def build_model(input_shape=Config.INPUT_SHAPE, num_classes=Config.NUM_CLASSES, learning_rate=Config.LEARNING_RATE):
    """
    Construct MobileNetV2 Transfer Learning Model.
    """
    logger.info("Initializing MobileNetV2 backbone pre-trained on ImageNet...")
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=input_shape
    )
    
    # Freeze the base feature extractor layers
    base_model.trainable = False
    
    x = base_model.output
    x = GlobalAveragePooling2D(name='global_avg_pool')(x)
    x = Dense(256, activation='relu', name='dense_256')(x)
    x = Dropout(0.3, name='dropout_0.3')(x)
    outputs = Dense(num_classes, activation='softmax', name='classification_head')(x)
    
    model = Model(inputs=base_model.input, outputs=outputs, name='HematoVision_MobileNetV2')
    
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(
        optimizer=optimizer,
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    logger.info("Model compiled successfully.")
    return model

def train_model(dataset_dir=Config.DATASET_DIR, epochs=Config.EPOCHS, batch_size=Config.BATCH_SIZE):
    """
    Train the blood cell classification model.
    """
    Config.init_app()
    logger.info(f"Starting model training pipeline with dataset at {dataset_dir}...")
    
    train_gen, val_gen = get_data_generators(dataset_dir, Config.IMAGE_SIZE, batch_size)
    model = build_model()
    
    callbacks = [
        ModelCheckpoint(
            filepath=str(Config.MODEL_PATH),
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=3,
            min_lr=1e-6,
            verbose=1
        )
    ]
    
    history = model.fit(
        train_gen,
        epochs=epochs,
        validation_data=val_gen,
        callbacks=callbacks
    )
    
    logger.info(f"Model training complete. Best model saved to {Config.MODEL_PATH}")
    return model, history

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train HematoVision Blood Cell Classification Model")
    parser.add_argument("--epochs", type=int, default=Config.EPOCHS, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=Config.BATCH_SIZE, help="Batch size for training")
    args = parser.parse_args()
    
    train_model(epochs=args.epochs, batch_size=args.batch_size)
