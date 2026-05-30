"""
PyInspiroBot
============

A Python package to interact with InspiroBot (https://inspirobot.me/).

Example usage:

    >>> from pyinspirobot import InspiroBot
    >>> bot = InspiroBot()
    >>> image_url = bot.get_image_url()
    >>> print(image_url)
    'https://generated.inspirobot.me/a/abcde12345.jpg'

    >>> image_data = bot.get_image()
    >>> with open('inspirobot.jpg', 'wb') as f:
    ...     f.write(image_data)

"""

import requests
from typing import Optional, Union

class InspiroBot:
    """Main class to interact with InspiroBot."""

    def __init__(self):
        self.base_url = "https://inspirobot.me/api/"

    def get_image_url(self, season: Optional[str] = None) -> str:
        """
        Get the URL of a generated inspirational image.

        Args:
            season (str, optional): Set to 'xmas' for Christmas-themed images.

        Returns:
            str: The absolute URL of the image.

        Raises:
            requests.RequestException: If the request fails.
        """
        params = {'generate': 'true'}
        if season:
            params['season'] = season

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        image_url = response.text.strip()

        # Ensure the URL is absolute
        if image_url.startswith('//'):
            image_url = 'https:' + image_url
        elif image_url.startswith('/'):
            image_url = 'https://inspirobot.me' + image_url

        return image_url

    def get_image(self, season: Optional[str] = None) -> bytes:
        """
        Get the binary content of a generated inspirational image.

        Args:
            season (str, optional): Set to 'xmas' for Christmas-themed images.

        Returns:
            bytes: The image data.

        Raises:
            requests.RequestException: If any of the requests fail.
        """
        image_url = self.get_image_url(season=season)
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        return image_response.content

# Convenience functions for simple use
def get_image_url(season: Optional[str] = None) -> str:
    """Convenience function to get an image URL using a default InspiroBot instance."""
    return InspiroBot().get_image_url(season=season)

def get_image(season: Optional[str] = None) -> bytes:
    """Convenience function to get an image using a default InspiroBot instance."""
    return InspiroBot().get_image(season=season)