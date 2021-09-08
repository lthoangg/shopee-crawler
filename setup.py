#!/usr/bin/env python
import setuptools

setuptools.setup(
    name='shopee-crawler',
    version='0.0.1',
    description='Crawler for shopee',
    author='Lê Trọng Hoàng',
    author_email='letronghoang00@gmail.com',
    url="https://github.com/lthoangg/shopee-crawler",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",  
)
