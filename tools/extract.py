import anthropic
import base64
import json


def extract_receipt(image_base64: str, media_type: str = "image/jpeg") -> dict:
    """
    Extract structured data from a receipt image.
    Pass the image as a base64 encoded string and its media type.
    """
    client = anthropic.Anthropic()

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
                            "data": image_base64
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