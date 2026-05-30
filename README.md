# PyInspiroBot

A Python package to interact with InspiroBot (https://inspirobot.me/).

## Installation

```bash
pip install pyinspirobot
```

## Usage

```python
from pyinspirobot import InspiroBot, get_image_url, get_image

# Using the class
bot = InspiroBot()
image_url = bot.get_image_url()
print(image_url)  # e.g., 'https://generated.inspirobot.me/a/abcde12345.jpg'

# Get Christmas-themed image
xmas_url = bot.get_image_url(season='xmas')

# Get the image data
image_data = bot.get_image()
with open('inspirobot.jpg', 'wb') as f:
    f.write(image_data)

# Using convenience functions
url = get_image_url()
img_data = get_image()
```

## API

### InspiroBot

- `get_image_url(season: Optional[str] = None) -> str`
- `get_image(season: Optional[str] = None) -> bytes`

### Convenience functions

- `get_image_url(season: Optional[str] = None) -> str`
- `get_image(season: Optional[str] = None) -> bytes`

## License

MIT