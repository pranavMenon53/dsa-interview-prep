'''
Why does this script exist?
The V2 document was converted from a Word document to Markdown using Pandoc. Pandoc does not support the width and height attributes for images, so this script converts the image syntax to HTML <img> tags with the correct width and height in pixels.
'''

from pathlib import Path
import re

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

INPUT_FILE = "./graph/output.md"
OUTPUT_FILE = "output.md"

DPI = 96  # CSS pixels per inch


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def inches_to_pixels(value: str) -> int:
    """Convert a string like '6.6412' to pixels."""
    return round(float(value) * DPI)


def replace_image(match: re.Match) -> str:
    alt = match.group("alt").replace("\n", " ").strip()
    src = match.group("src").strip()

    width = inches_to_pixels(match.group("width"))
    height = inches_to_pixels(match.group("height"))

    alt_attr = f' alt="{alt}"' if alt else ""

    return (
        f'<img src="{src}"{alt_attr} '
        f'width="{width}" '
        f'height="{height}">'
    )


# -----------------------------------------------------------------------------
# Pattern
# -----------------------------------------------------------------------------

IMAGE_PATTERN = re.compile(
    r"""
    !\[
        (?P<alt>.*?)                # alt text (can span lines)
    \]
    \(
        (?P<src>[^)]+?)             # image path
    \)
    \{
        .*?
        width="(?P<width>[\d.]+)in"
        .*?
        height="(?P<height>[\d.]+)in"
        .*?
    \}
    """,
    re.DOTALL | re.VERBOSE,
)


# -----------------------------------------------------------------------------
# Convert
# -----------------------------------------------------------------------------

markdown = Path(INPUT_FILE).read_text(encoding="utf-8")

converted = IMAGE_PATTERN.sub(replace_image, markdown)

Path(OUTPUT_FILE).write_text(converted, encoding="utf-8")

print("Done!")
print(f"Output written to {OUTPUT_FILE}")