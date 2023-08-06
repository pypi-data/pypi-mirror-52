from pathlib import Path

import setuptools

from freeotp_extractor import __version__, __author__

ROOT = Path(__file__).resolve().parent

readme_path = ROOT / "README.md"

setuptools.setup(
    name="freeotp-extractor",
    version=__version__,
    author=__author__.split(" <")[0],
    author_email=__author__.split(" <")[1].strip("<>"),
    description="Extract tokens from FreeOTP backup",
    long_description=readme_path.read_text(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Oprax/freeotp-extractor",
    packages=setuptools.find_packages(),
    install_requires=["pyqrcode", "awesome-slugify"],
    license="MIT",
    entry_points={"console_scripts": ["freeotp-extractor = freeotp_extractor:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Operating System :: POSIX",
    ],
)
