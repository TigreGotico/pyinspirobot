"""
Basic usage examples for pyinspirobot
"""

import pyinspirobot
import os

def main():
    # Create an InspiroBot instance
    bot = pyinspirobot.InspiroBot()
    
    # Example 1: Get a random inspirational image URL
    print("=== Example 1: Getting Image URL ===")
    image_url = bot.get_image_url()
    print(f"Image URL: {image_url}")
    
    # Example 2: Get a Christmas-themed image URL
    print("\n=== Example 2: Getting Christmas Image URL ===")
    christmas_url = bot.get_image_url(season='xmas')
    print(f"Christmas Image URL: {christmas_url}")
    
    # Example 3: Get the actual image data and save it
    print("\n=== Example 3: Downloading and Saving Image ===")
    image_data = bot.get_image()
    
    # Save to file
    with open('inspirobot_example.jpg', 'wb') as f:
        f.write(image_data)
    print(f"Saved image to inspirobot_example.jpg ({len(image_data)} bytes)")
    
    # Example 4: Using convenience functions
    print("\n=== Example 4: Using Convenience Functions ===")
    url = pyinspirobot.get_image_url()
    img_data = pyinspirobot.get_image()
    
    with open('convenience_example.jpg', 'wb') as f:
        f.write(img_data)
    print(f"Saved convenience example to convenience_example.jpg ({len(img_data)} bytes)")
    
    print("\n=== All examples completed successfully! ===")

if __name__ == "__main__":
    main()