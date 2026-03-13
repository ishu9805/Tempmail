from pathlib import Path

from setuptools import find_packages, setup

README = Path("README.md").read_text(encoding="utf-8")

setup(
    name="temp-gmail",
    version="1.1.0",
    author="zukixa",
    author_email="56563509+zukixa@users.noreply.github.com",
    description="Temp gmail API with Telegram bot + web inbox support.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/zukixa/temp-gmail",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=["curl-cffi>=0.7.3", "pyrogram>=2.0.106", "tgcrypto>=1.2.5", "flask>=3.0.0"],
)
