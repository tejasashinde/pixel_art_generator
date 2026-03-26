# pixel_art_converter/core.py

from PIL import Image
import numpy as np
from .palettes import PALETTES

# ------------------------------
# Low-level quantization
# ------------------------------

def closest_color(pixel: np.ndarray, palette: list[tuple[int, int, int]]) -> tuple[int,int,int]:
    palette = np.array(palette)
    pixel = np.array(pixel)
    distances = np.sum((palette - pixel) ** 2, axis=1)
    return tuple(palette[np.argmin(distances)])

def quantize_with_palette(img_data: np.ndarray, palette: list[tuple[int,int,int]]) -> np.ndarray:
    return np.array([[closest_color(pixel, palette) for pixel in row] for row in img_data])

def quantize_8bit_vectorized(img_data: np.ndarray) -> np.ndarray:
    # Round each channel down to nearest multiple of 32 (8-bit style)
    return (img_data // 32 * 32).astype(np.uint8)

def quantize_image(
    image_path: str,
    output_path: str,
    palette: list[tuple[int,int,int]] = None,
    resize_factor: int = 4,
    quantize_fn = None
):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((img.width // resize_factor, img.height // resize_factor), Image.NEAREST)
    img_data = np.array(img)

    if quantize_fn:
        quantized = quantize_fn(img_data)
    elif palette:
        quantized = quantize_with_palette(img_data, palette)
    else:
        raise ValueError("Must provide either a palette or quantization function")

    Image.fromarray(quantized.astype(np.uint8)).save(output_path)

# ------------------------------
# High-level style conversion
# ------------------------------

def convert_to_palette_style(image_path: str, output_path: str, style: str, resize_factor: int = 4):
    if style not in PALETTES:
        raise ValueError(f"Unknown style '{style}'. Available: {list(PALETTES.keys())}")
    palette = PALETTES[style]
    quantize_image(image_path, output_path, palette=palette, resize_factor=resize_factor)

def convert_to_style(image_path: str, output_path: str, style: str = None, resize_factor: int = 4):
    """
    Generic style converter:
    - style=None => defaults to 8-bit
    - style in PALETTES => use palette
    """
    if style is None:
        # default 8-bit quantization
        quantize_image(image_path, output_path, resize_factor=resize_factor, quantize_fn=quantize_8bit_vectorized)
    else:
        convert_to_palette_style(image_path, output_path, style.lower(), resize_factor=resize_factor)
