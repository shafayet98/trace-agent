import anthropic
import base64
import json
from pathlib import Path


async def extract_receipt(image_path: str) -> dict:
    """
    Extract structured data from a receipt image.
    Provide the full path to the image file.
    """
    client = anthropic.Anthropic()

    # Read and encode image
    image_data = Path(image_path).read_bytes()
    b64_image = base64.standard_b64encode(image_data).decode("utf-8")

    # Detect media type
    suffix = Path(image_path).suffix.lower()
    media_type_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp"
    }
    media_type = media_type_map.get(suffix, "image/jpeg")

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": b64_image
                        }
                    },
                    {
                        "type": "text",
                        "text": """Extract the following from this receipt and return ONLY valid JSON, no other text:
                        {
                            "date": "YYYY-MM-DD",
                            "merchant": "store name",
                            "category": "one of: groceries, dining, transport, entertainment, health, shopping, utilities, other",
                            "total": 0.00,
                            "items": [{"name": "item name", "price": 0.00}]
                        }
                        If any field is unclear, make your best guess. For date, use today if not visible."""
                    }
                ]
            }
        ]
    )

    raw = response.content[0].text.strip()
    return json.loads(raw)
