from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyinspirobot",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python package to interact with InspiroBot (https://inspirobot.me/)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LeMetadatarr/pyinspirobot",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
)