# InspiroBot API Reference

## Overview
InspiroBot (https://inspirobot.me/) is an artificial intelligence that generates unique inspirational quotes. Through reverse engineering, we've identified the core API endpoint used to generate these images.

## Base URL
```
https://inspirobot.me/api/
```

## Endpoints

### Generate Image
**GET** `/api/`

Returns a direct URL to a generated inspirational image.

#### Query Parameters
- `generate` (required): Must be set to `"true"`
- `season` (optional): Set to `"xmas"` for Christmas-themed images

#### Response
- **Content-Type**: `text/plain`
- **Body**: A URL string pointing to the generated image (typically a JPEG)

#### Example Request
```
GET https://inspirobot.me/api/?generate=true
```

#### Example Response
```
https://generated.inspirobot.me/a/abcde12345.jpg
```

#### Example with Season
```
GET https://inspirobot.me/api/?generate=true&season=xmas
```

#### Example Response
```
https://generated.xmascardbot.com/xmas010/aXm1179xjU.jpg
```

## Image URLs
The generated image URLs follow these patterns:
- Standard: `https://generated.inspirobot.me/a/[ID].jpg`
- Christmas: `https://generated.xmascardbot.com/xmas[ID]/[ID].jpg`

Where `[ID]` is a unique identifier string.

## Direct Image Access
Once you have the image URL from the API, you can directly access the image data:
```
GET https://generated.inspirobot.me/a/abcde12345.jpg
```
Returns the binary image data with appropriate `Content-Type` header (usually `image/jpeg`).

## Rate Limiting & Usage
InspiroBot does not appear to have strict rate limiting for personal use, but please:
- Use reasonable request frequencies
- Consider caching results when appropriate
- Respect the service and its intended purpose
- Do not use for commercial purposes without permission

## Technical Notes
- The service appears to run on multiple servers/regions
- Images are hosted on AWS S3-like storage (generated.inspirobot.me)
- Christmas images may be served from a different domain (generated.xmascardbot.com)
- The API does not require authentication
- Image generation appears to be truly random/unique each time

## Error Handling
If the service is unavailable or experiencing issues:
- HTTP status codes may vary (503, 500, etc.)
- Response body may contain error messages
- Implement retry logic with exponential backoff for production use

## Related Endpoints (Discovered but not confirmed for public use)
During reverse engineering, these endpoints were observed in the JavaScript but may not be part of the public API:
- `/share?iuid=[ID]` - Used for sharing generated images
- Various asset endpoints for CSS, JS, and images

These are not recommended for use as they may change without notice.

## Example Usage in Python
```python
import requests

def get_inspirobot_url(season=None):
    """Get an inspirational image URL from InspiroBot."""
    params = {'generate': 'true'}
    if season:
        params['season'] = season
    
    response = requests.get('https://inspirobot.me/api/', params=params)
    response.raise_for_status()
    return response.text.strip()

def get_inspirobot_image(season=None):
    """Get the binary image data from InspiroBot."""
    url = get_inspirobot_url(season=season)
    image_response = requests.get(url)
    image_response.raise_for_status()
    return image_response.content

# Usage
image_url = get_inspirobot_url()
print(f"Image URL: {image_url}")

image_data = get_inspirobot_image()
with open('inspirobot.jpg', 'wb') as f:
    f.write(image_data)
```