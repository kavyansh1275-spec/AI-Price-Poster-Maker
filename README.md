# AI Price Poster Maker

AI-assisted sale creative, price comparison, bulk branded poster generation, and AI creative variations for local shops and small businesses.

## Features

### V1 — Sale Poster
- Upload a product photo
- Enter product name, MRP, and sale price
- Automatically calculate discount
- Choose poster templates
- Preview and download PNG

### V2 — AI Creative
- Local Ollama marketing-copy generation
- Deterministic fallback when Ollama is unavailable
- Instagram post, portrait, and landscape formats

### V3 — Price Comparison
- Compare prices across stores
- Import comparison CSVs
- Highlight cheapest option and maximum savings
- Generate comparison poster

### V4 — Batch Business Mode
- Import product catalog CSV
- Match multiple product images by filename
- Apply business name and brand color
- Add optional logo
- Generate a complete poster set
- Download every poster as one ZIP

### V5 — AI Creative Lab
- Generate three distinct promotional variations from one product image
- Flash Sale, Weekend Deal, and Premium Offer designs
- Reuse AI-generated headline and CTA
- Download each variation separately

## Run locally

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### V4 catalog format

```csv
name,mrp,sale_price,image_name
Running Shoes,2999,1999,shoes.jpg
Travel Bag,1999,1299,bag.png
```

The `image_name` values must match uploaded product filenames.

## Roadmap
- V1: Core poster maker
- V2: AI copy and social formats
- V3: Price comparison / price intelligence
- V4: Batch generation and brand kits
- V5: AI creative variations and stronger image processing
- V6: Production deployment and performance polish
- V7: Monetization-ready local-business workflow
