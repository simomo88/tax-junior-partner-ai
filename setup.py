"""Setup script for Tax Junior Partner AI."""

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="tax-junior-partner-ai",
    version="0.1.0",
    author="Simomo88",
    description="Personal tax assistant for Italian tax professionals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simomo88/tax-junior-partner-ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Legal Industry",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=[
        line.strip()
        for line in (this_directory / "requirements.txt").read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ],
)
