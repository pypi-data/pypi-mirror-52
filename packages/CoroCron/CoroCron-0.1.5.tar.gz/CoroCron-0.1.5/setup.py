import io
import CoroCron
from setuptools import setup, find_packages

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except:
    long_description = ""

setup(
    name = "CoroCron",
    version = CoroCron.__version__,
    author = "Flying Kiwi",
    author_email = "github@flyingkiwibird.com",
    description = ("A pythonic cron using asyncio"),
    license = "MIT",
    keywords = "Cron asyncio schedule",
    url = "https://github.com/FlyingKiwiBird/AioCron",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "examples", "examples.*"]),
    install_requires=[],
    long_description_content_type='text/markdown',
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
