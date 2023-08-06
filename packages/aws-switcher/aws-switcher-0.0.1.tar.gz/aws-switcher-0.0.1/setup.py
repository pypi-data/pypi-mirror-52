from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="aws-switcher",
    version="0.0.1",
    author="GDantas",
    author_email="gabriel-dantasg98@gmail.com",
    license="MIT License",
    description="A simple cli to switch aws credentials",
    long_description_content_type='text/markdown',
    long_description=long_description,
    url="https://github.com/gabriel-dantas98/gtools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
