import cv2
import numpy as np
from typing import Tuple, Union
from pathlib import Path
from config import Config

def validate_image(file_path: Union[str, Path]) -> bool:
    """Check if the given file path is a readable, non-corrupted image."""
    try:
        path_str = str(file_path)
        img = cv2.imread(path_str)
        if img is None or img.size == 0:
            return False
        return True
    except Exception:
        return False

def load_and_preprocess_image(
    file_path: Union[str, Path], 
    target_size: Tuple[int, int] = Config.IMAGE_SIZE
) -> np.ndarray:
    """
    Load an image from disk, convert to RGB, resize, scale to [0, 1],
    and expand dimensions to batch format (1, 224, 224, 3).
    """
    path_str = str(file_path)
    img_bgr = cv2.imread(path_str)
    if img_bgr is None:
        raise ValueError(f"Could not read image file from path: {file_path}")
        
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, target_size)
    img_normalized = img_resized.astype(np.float32) / 255.0
    img_batch = np.expand_dims(img_normalized, axis=0)
    return img_batch

def get_data_generators(
    dataset_dir: Union[str, Path] = Config.DATASET_DIR,
    image_size: Tuple[int, int] = Config.IMAGE_SIZE,
    batch_size: int = Config.BATCH_SIZE
):
    """
    Construct Keras ImageDataGenerators for training and validation with data augmentation.
    """
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    
    dataset_path = Path(dataset_dir)
    train_dir = dataset_path / 'train'
    val_dir = dataset_path / 'val'
    
    train_datagen = ImageDataGenerator(
        rescale=1.0/255.0,
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    val_datagen = ImageDataGenerator(rescale=1.0/255.0)
    
    train_generator = train_datagen.flow_from_directory(
        directory=str(train_dir),
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=True
    )
    
    val_generator = val_datagen.flow_from_directory(
        directory=str(val_dir),
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )
    
    return train_generator, val_generator
