#!/usr/bin/env python3
"""Test script for pyinspirobot."""

from pyinspirobot import InspiroBot, get_image_url, get_image

def test_class():
    print("Testing InspiroBot class...")
    bot = InspiroBot()
    url = bot.get_image_url()
    print(f"Image URL: {url}")
    assert url.startswith('https://'), f"URL should start with https://, got {url}"
    print("✓ get_image_url works")

    # Test with season
    xmas_url = bot.get_image_url(season='xmas')
    print(f"Xmas Image URL: {xmas_url}")
    assert xmas_url.startswith('https://'), f"Xmas URL should start with https://, got {xmas_url}"
    print("✓ get_image_url with season works")

    # Test get_image (just check that we get bytes)
    img_data = bot.get_image()
    print(f"Image data length: {len(img_data)} bytes")
    assert isinstance(img_data, bytes), f"Expected bytes, got {type(img_data)}"
    assert len(img_data) > 0, "Image data should not be empty"
    print("✓ get_image works")

def test_convenience_functions():
    print("\nTesting convenience functions...")
    url = get_image_url()
    print(f"Image URL via function: {url}")
    assert url.startswith('https://'), f"URL should start with https://, got {url}"
    print("✓ get_image_url function works")

    img_data = get_image()
    print(f"Image data length via function: {len(img_data)} bytes")
    assert isinstance(img_data, bytes), f"Expected bytes, got {type(img_data)}"
    assert len(img_data) > 0, "Image data should not be empty"
    print("✓ get_image function works")

if __name__ == '__main__':
    test_class()
    test_convenience_functions()
    print("\n🎉 All tests passed!")