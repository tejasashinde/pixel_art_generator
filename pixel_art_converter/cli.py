# pixel_art_converter/cli.py

import argparse
from pathlib import Path
from .core import convert_to_style, generate_palette_preview, list_palette_names
from .palettes import PALETTES

def main():
    parser = argparse.ArgumentParser(
        description="Convert an image to retro pixel-art style."
    )
    parser.add_argument("-i", "--input", help="Path to input image")
    parser.add_argument("-o", "--output", help="Path to output image (without style suffix)")
    parser.add_argument(
        "--style", help=f"Pixel art style. Available: {list(PALETTES.keys())}", default=None
    )
    parser.add_argument("--resize", type=int, help="Resize factor (default 4)", default=4)
    parser.add_argument(
        "--dither",
        choices=["none", "ordered", "floyd-steinberg"],
        default="none",
        help="Dithering mode (default none)",
    )
    parser.add_argument("--list-styles", action="store_true", help="List all available palette styles and exit")
    parser.add_argument(
        "--preview-palettes",
        metavar="PREVIEW",
        help="Generate a palette preview image and exit",
    )

    args = parser.parse_args()

    if args.list_styles:
        for name in list_palette_names():
            print(name)
        return

    if args.preview_palettes:
        generate_palette_preview(args.preview_palettes)
        print(f"Palette preview saved to {args.preview_palettes}")
        return

    if not args.input or not args.output:
        parser.error("the following arguments are required unless --list-styles or --preview-palettes is used: -i/--input, -o/--output")

    input_path = Path(args.input)
    output_path = Path(args.output)

    # Append _style to output filename if style is passed
    if args.style:
        output_file = output_path.stem + f"_{args.style.lower()}" + output_path.suffix
        output_path = output_path.parent / output_file

    convert_to_style(
        str(input_path),
        str(output_path),
        style=args.style,
        resize_factor=args.resize,
        dither=args.dither,
    )
    print(f"Image saved to {output_path}")

if __name__ == "__main__":
    main()
