#!/usr/bin/env python
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='shopee_crawler-pkg-lthoangg',
    version='0.0.1',
    author='Lê Trọng Hoàng',
    author_email='letronghoang00@gmail.com',
    description='Crawler for shopee',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lthoangg/shopee-crawler",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src/requirements.txt"),
    python_requires=">=3.7",  
)
