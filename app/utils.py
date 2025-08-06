from PIL import Image as PILImage
from pathlib import Path

# Placeholder AI tagging

def analyze_image(image_path: Path):
    # For demo, just return dummy data based on filename
    name = image_path.stem.lower()
    species = None
    if "deer" in name:
        species = "deer"
    elif "turkey" in name:
        species = "turkey"
    elif "coyote" in name:
        species = "coyote"

    antler_class = None
    if species == "deer":
        if "8" in name:
            antler_class = "8-point"
        elif "spike" in name:
            antler_class = "spike"
        elif "doe" in name:
            antler_class = "doe"

    # Determine time of day using simple brightness heuristic
    try:
        im = PILImage.open(image_path)
        grayscale = im.convert("L")
        brightness = sum(grayscale.getdata()) / (255 * im.width * im.height)
        if brightness > 0.6:
            tod = "day"
        elif brightness < 0.3:
            tod = "night"
        else:
            tod = "dawn/dusk"
    except Exception:
        tod = None

    return species, antler_class, tod
