# pixel_art_converter/tests/test_core.py

import numpy as np
from pathlib import Path
from PIL import Image

from ..core import generate_palette_preview, list_palette_names, quantize_8bit_vectorized, quantize_image, quantize_with_palette

def test_quantize_with_palette_simple():
    img_data = np.array([[[10, 10, 10], [250, 250, 250]]])
    palette = [(0,0,0), (255,255,255)]
    result = quantize_with_palette(img_data, palette)
    assert (result[0,0] == [0,0,0]).all()
    assert (result[0,1] == [255,255,255]).all()

def test_quantize_8bit_vectorized():
    img_data = np.array([[[45, 100, 200]]])
    result = quantize_8bit_vectorized(img_data)
    assert (result[0,0] == [32,96,192]).all()

def test_list_palette_names_includes_new_styles():
    names = list_palette_names()
    assert "metroid" in names
    assert "pokemon_gb" in names
    assert "chrono_trigger" in names
    assert "pokemon_red" in names
    assert "earthbound" in names
    assert "super_mario_world" in names
    assert "mortal_kombat" in names
    assert len(names) == 50

def test_generate_palette_preview(tmp_path):
    preview_path = Path(tmp_path) / "preview.png"
    generate_palette_preview(str(preview_path), style_names=["mario", "zelda"])
    assert preview_path.exists()
    img = Image.open(preview_path)
    assert img.size[0] > 0
    assert img.size[1] > 0

def test_quantize_image_preserves_alpha(tmp_path):
    input_path = Path(tmp_path) / "input.png"
    output_path = Path(tmp_path) / "output.png"

    img = Image.new("RGBA", (4, 4), (200, 50, 100, 123))
    img.save(input_path)

    quantize_image(str(input_path), str(output_path), quantize_fn=quantize_8bit_vectorized)

    result = Image.open(output_path)
    assert result.mode == "RGBA"
    assert result.size == (4, 4)
    assert result.getpixel((0, 0))[3] == 123

def test_quantize_image_keeps_output_size(tmp_path):
    input_path = Path(tmp_path) / "input_rgb.png"
    output_path = Path(tmp_path) / "output_rgb.png"

    img = Image.new("RGB", (12, 8), (200, 50, 100))
    img.save(input_path)

    quantize_image(str(input_path), str(output_path), quantize_fn=quantize_8bit_vectorized)

    result = Image.open(output_path)
    assert result.size == (12, 8)
