from setuptools import setup, find_packages

setup(
    name="vibedrop-ai",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "mido",
    ],
    python_requires=">=3.8",
)
