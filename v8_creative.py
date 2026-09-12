from PIL import Image

from creative_engine import generate_variations
from image_ai import prepare_product_image


def generate_enhanced_variations(image: Image.Image, product_name: str, mrp: float, sale_price: float, discount: int, headline: str, cta: str):
    """Generate V5 creative layouts after lightweight local image enhancement."""
    prepared = prepare_product_image(image)
    return generate_variations(prepared, product_name, mrp, sale_price, discount, headline, cta)
