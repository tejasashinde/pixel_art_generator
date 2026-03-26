# pixel_art_converter/cli.py

import argparse
from pathlib import Path
from .core import convert_to_style
from .palettes import PALETTES

def main():
    parser = argparse.ArgumentParser(
        description="Convert an image to retro pixel-art style."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to input image")
    parser.add_argument("-o", "--output", required=True, help="Path to output image (without style suffix)")
    parser.add_argument(
        "--style", help=f"Pixel art style. Available: {list(PALETTES.keys())}", default=None
    )
    parser.add_argument("--resize", type=int, help="Resize factor (default 4)", default=4)

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    # Append _style to output filename if style is passed
    if args.style:
        output_file = output_path.stem + f"_{args.style.lower()}" + output_path.suffix
        output_path = output_path.parent / output_file

    convert_to_style(str(input_path), str(output_path), style=args.style, resize_factor=args.resize)
    print(f"Image saved to {output_path}")

if __name__ == "__main__":
    main()
