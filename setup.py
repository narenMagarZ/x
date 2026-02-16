from setuptools import setup

setup(
    name="x",
    version="1.0",
    packages=["src"],
    author="naren magar",
    entry_points={
        "console_scripts": ["x = src.main:main"]
    },
    description="prompt based cli",
    python_requires=">=3.6",
)