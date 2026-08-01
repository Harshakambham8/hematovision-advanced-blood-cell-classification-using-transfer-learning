import cv2
import numpy as np
import logging
from pathlib import Path
from typing import Tuple, Optional, Union
from config import Config

logger = logging.getLogger(__name__)

def generate_gradcam_heatmap(
    model, 
    img_array: np.ndarray, 
    pred_index: Optional[int] = None, 
    layer_name: Optional[str] = None
) -> np.ndarray:
    import tensorflow as tf
    """
    Generate Grad-CAM heatmap array for a given model and input image.
    """
    if layer_name is None:
        # Auto-detect last 4D convolutional layer
        for layer in reversed(model.layers):
            if len(layer.output_shape) == 4 and ('conv' in layer.name.lower() or 'relu' in layer.name.lower() or 'out' in layer.name.lower()):
                layer_name = layer.name
                break
                
    if not layer_name:
        # Fallback layer name for MobileNetV2
        layer_name = 'Conv_1' if 'Conv_1' in [l.name for l in model.layers] else model.layers[-4].name

    grad_model = tf.keras.models.Model(
        inputs=[model.inputs],
        outputs=[model.get_layer(layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(predictions[0])
        class_channel = predictions[:, pred_index]

    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0) / (tf.reduce_max(heatmap) + 1e-10)
    return heatmap.numpy()

def save_gradcam_overlay(
    original_image_path: Union[str, Path], 
    heatmap: np.ndarray, 
    output_path: Union[str, Path], 
    alpha: float = 0.5
) -> str:
    """
    Superimpose Grad-CAM heatmap over the original image and save to disk.
    """
    img_bgr = cv2.imread(str(original_image_path))
    if img_bgr is None:
        raise ValueError(f"Unable to read image at {original_image_path}")

    height, width = img_bgr.shape[:2]
    
    # Resize heatmap to match image dimensions
    heatmap_resized = cv2.resize(heatmap, (width, height))
    heatmap_uint8 = np.uint8(255 * heatmap_resized)
    
    # Apply JET color map
    color_heatmap = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    
    # Superimpose heatmap on original image
    overlay = cv2.addWeighted(color_heatmap, alpha, img_bgr, 1 - alpha, 0)
    
    output_str = str(output_path)
    Path(output_str).parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(output_str, overlay)
    logger.info(f"Saved Grad-CAM overlay to {output_str}")
    return output_str
