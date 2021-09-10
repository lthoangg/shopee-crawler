import os
import setuptools
from configparser import ConfigParser

try:
    # pip >=20
    from pip._internal.network.session import PipSession
    from pip._internal.req import parse_requirements
except ImportError:
    try:
        # 10.0.0 <= pip <= 19.3.1
        from pip._internal.download import PipSession
        from pip._internal.req import parse_requirements
    except ImportError:
        # pip <= 9.0.3
        from pip.download import PipSession
        from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session=False)
try:
    reqs = [str(ir.req) for ir in install_reqs]
except:
    reqs = [str(ir.requirement) for ir in install_reqs]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


parser = ConfigParser()
parser.read('config.ini')
config = parser['setup']

setuptools.setup(
    name=config['name'],
    version=config['version'],
    author=config['author'],
    author_email=config['author_email'],
    description=config['description'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=config["url"],
    packages=setuptools.find_packages(),
    install_requires=reqs,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=config['python_requires'],  
)
