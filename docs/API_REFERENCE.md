# InspiroBot API Reference

## Overview

[InspiroBot](https://inspirobot.me/) is a service that generates inspirational quote images. This reference describes the API endpoint that the service uses to generate these images.

## Base URL

```
https://inspirobot.me/api/
```

## Endpoints

### Generate Image

**GET** `/api/`

Returns a direct URL to a generated image.

#### Query Parameters

- `generate` (required): Set to `"true"`.
- `season` (optional): Set to `"xmas"` for a Christmas-themed image.

#### Response

- **Content-Type**: `text/plain`
- **Body**: A URL string that points to the generated image (typically a JPEG).

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

`[ID]` is a unique identifier string.

## Direct Image Access

Once you have the image URL from the API, you can access the image data directly:

```
GET https://generated.inspirobot.me/a/abcde12345.jpg
```

This returns the binary image data with a `Content-Type` header, usually `image/jpeg`.

## Rate Limiting and Usage

InspiroBot does not enforce strict rate limiting for personal use. Use reasonable request frequencies, cache results when you can, and do not use the service for commercial purposes without permission.

## Technical Notes

- The service runs on multiple servers or regions.
- Images are hosted on AWS S3-like storage (`generated.inspirobot.me`).
- Christmas images may come from a different domain (`generated.xmascardbot.com`).
- The API does not require authentication.
- Each generated image is unique.

## Error Handling

If the service is unavailable, the HTTP status code may vary (503, 500, or others) and the response body may contain an error message. For production use, add retry logic with exponential backoff.

## Related Endpoints

These endpoints appear in the service's JavaScript but are not confirmed as public API:

- `/share?iuid=[ID]` — used for sharing generated images
- Various asset endpoints for CSS, JS, and images

Do not rely on these endpoints. They may change without notice.

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
