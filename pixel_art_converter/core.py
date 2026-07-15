# pixel_art_converter/core.py

from PIL import Image, ImageDraw, ImageFont
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

def quantize_8bit_pixel(pixel: np.ndarray) -> np.ndarray:
    return (np.array(pixel) // 32 * 32).astype(np.uint8)

def quantize_8bit_vectorized(img_data: np.ndarray) -> np.ndarray:
    # Round each channel down to nearest multiple of 32 (8-bit style)
    return (img_data // 32 * 32).astype(np.uint8)

def apply_ordered_dither(img_data: np.ndarray, strength: int = 32) -> np.ndarray:
    bayer_4x4 = np.array(
        [
            [0, 8, 2, 10],
            [12, 4, 14, 6],
            [3, 11, 1, 9],
            [15, 7, 13, 5],
        ],
        dtype=np.float32,
    )
    threshold_map = (bayer_4x4 / 16.0 - 0.5) * strength
    tiled = np.tile(threshold_map, (img_data.shape[0] // 4 + 1, img_data.shape[1] // 4 + 1))
    offset = tiled[: img_data.shape[0], : img_data.shape[1]][:, :, None]
    return np.clip(img_data.astype(np.float32) + offset, 0, 255).astype(np.uint8)

def quantize_with_floyd_steinberg(img_data: np.ndarray, quantize_pixel_fn) -> np.ndarray:
    working = img_data.astype(np.float32).copy()
    height, width = working.shape[:2]

    for y in range(height):
        for x in range(width):
            old_pixel = working[y, x].copy()
            new_pixel = np.array(quantize_pixel_fn(old_pixel), dtype=np.float32)
            working[y, x] = new_pixel
            error = old_pixel - new_pixel

            if x + 1 < width:
                working[y, x + 1] += error * 7 / 16
            if y + 1 < height:
                if x > 0:
                    working[y + 1, x - 1] += error * 3 / 16
                working[y + 1, x] += error * 5 / 16
                if x + 1 < width:
                    working[y + 1, x + 1] += error * 1 / 16

    return np.clip(working, 0, 255).astype(np.uint8)

def quantize_image(
    image_path: str,
    output_path: str,
    palette: list[tuple[int,int,int]] = None,
    resize_factor: int = 4,
    quantize_fn = None,
    dither: str = "none",
):
    if resize_factor <= 0:
        raise ValueError("resize_factor must be greater than 0")

    img = Image.open(image_path)
    has_alpha = "A" in img.getbands()
    original_size = img.size
    img = img.convert("RGBA")
    resized_width = max(1, img.width // resize_factor)
    resized_height = max(1, img.height // resize_factor)
    img = img.resize((resized_width, resized_height), Image.NEAREST)

    img_data = np.array(img)
    rgb_data = img_data[:, :, :3]
    alpha_data = img_data[:, :, 3]

    if dither not in {"none", "ordered", "floyd-steinberg"}:
        raise ValueError("dither must be one of: none, ordered, floyd-steinberg")

    if dither == "ordered":
        rgb_data = apply_ordered_dither(rgb_data)

    if dither == "floyd-steinberg":
        if quantize_fn:
            quantized_rgb = quantize_with_floyd_steinberg(rgb_data, quantize_fn)
        elif palette:
            quantized_rgb = quantize_with_floyd_steinberg(rgb_data, lambda pixel: closest_color(pixel, palette))
        else:
            quantized_rgb = quantize_with_floyd_steinberg(rgb_data, quantize_8bit_pixel)
    elif quantize_fn:
        quantized_rgb = quantize_fn(rgb_data)
    elif palette:
        quantized_rgb = quantize_with_palette(rgb_data, palette)
    else:
        raise ValueError("Must provide either a palette or quantization function")

    if has_alpha:
        output = np.dstack((quantized_rgb.astype(np.uint8), alpha_data.astype(np.uint8)))
        final_image = Image.fromarray(output, mode="RGBA")
    else:
        final_image = Image.fromarray(quantized_rgb.astype(np.uint8), mode="RGB")

    if final_image.size != original_size:
        final_image = final_image.resize(original_size, Image.NEAREST)

    final_image.save(output_path)

def list_palette_names() -> list[str]:
    return sorted(PALETTES.keys())

def generate_palette_preview(
    output_path: str,
    style_names: list[str] | None = None,
    swatch_size: int = 24,
    padding: int = 12,
    label_width: int = 140,
):
    names = style_names or list_palette_names()
    font = ImageFont.load_default()
    line_height = swatch_size + 12
    width = label_width + padding + max(len(PALETTES[name]) for name in names) * swatch_size + padding
    height = padding + len(names) * line_height + padding
    canvas = Image.new("RGB", (width, height), (20, 20, 20))
    draw = ImageDraw.Draw(canvas)

    for index, name in enumerate(names):
        y = padding + index * line_height
        draw.text((padding, y + 4), name, fill=(240, 240, 240), font=font)
        x = padding + label_width
        for color in PALETTES[name]:
            draw.rectangle([x, y, x + swatch_size - 1, y + swatch_size - 1], fill=color)
            x += swatch_size

    canvas.save(output_path)

# ------------------------------
# High-level style conversion
# ------------------------------

def convert_to_palette_style(
    image_path: str,
    output_path: str,
    style: str,
    resize_factor: int = 4,
    dither: str = "none",
):
    if style not in PALETTES:
        raise ValueError(f"Unknown style '{style}'. Available: {list(PALETTES.keys())}")
    palette = PALETTES[style]
    quantize_image(image_path, output_path, palette=palette, resize_factor=resize_factor, dither=dither)

def convert_to_style(
    image_path: str,
    output_path: str,
    style: str = None,
    resize_factor: int = 4,
    dither: str = "none",
):
    """
    Generic style converter:
    - style=None => defaults to 8-bit
    - style in PALETTES => use palette
    """
    if style is None:
        # default 8-bit quantization
        quantize_image(
            image_path,
            output_path,
            resize_factor=resize_factor,
            quantize_fn=quantize_8bit_vectorized,
            dither=dither,
        )
    else:
        convert_to_palette_style(image_path, output_path, style.lower(), resize_factor=resize_factor, dither=dither)
