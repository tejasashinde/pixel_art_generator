# pixel_art_converter/tests/test_core.py

import numpy as np
from ..core import quantize_with_palette, quantize_8bit_vectorized

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
