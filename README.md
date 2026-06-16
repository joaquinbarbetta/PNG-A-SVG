# PNG-A-SVG

Converts raster images (PNG/JPG) to clean SVG vector files using OpenCV contour detection.

## How it works

Instead of tracing edges naively, the script analyzes the full contour hierarchy of the image to determine which shapes are "ink" and which are "holes" — this correctly handles cases like the inside of a letter or a donut shape.

- **Even depth** → filled shape (black)
- **Odd depth** → cutout / hole (white)

Contours are sorted by area and drawn largest-first, so smaller shapes are never accidentally covered.

## Usage

```bash
pip install opencv-python svgwrite numpy
python conversionsvg.py
```

Edit the last two lines in `conversionsvg.py` to point to your input image and desired output path:

```python
jpg_to_svg('your_image.png', 'output.svg')
```

## Dependencies

- `opencv-python`
- `svgwrite`
- `numpy`

## Limitations

Works best on high-contrast images (logos, icons, line art). Not designed for photographic content.
