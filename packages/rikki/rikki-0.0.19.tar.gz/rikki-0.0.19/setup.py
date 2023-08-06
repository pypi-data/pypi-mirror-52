import os
import sys

import setuptools
from setuptools.command.install import install


def version() -> str: return "0.0.19"


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != version():
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, version()
            )
            sys.exit(info)


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rikki",
    version=version(),
    author="Sergey Yamshchikov",
    author_email="yamsergey@gmail.com",
    description="A small runner script which allows to run behaviour tests backed by proxy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yamsergey/rikki",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    cmdclass={
        'verify': VerifyVersionCommand,
    },
    entry_points={
        'console_scripts': [
            "rikki = rikki.tools.main:rikki"
        ]
    },
    install_requires=[
        "allure-behave>=2.8.5",
        "allure-python-commons>=2.8.5",
        "Appium-Python-Client>=0.47",
        "asn1crypto>=0.24.0",
        "attrs>=19.1.0",
        "behave>=1.2.6",
        "bleach>=3.1.0",
        "blinker>=1.4",
        "brotlipy>=0.7.0",
        "certifi>=2019.6.16",
        "cffi>=1.12.3",
        "chardet>=3.0.4",
        "click>=6.7",
        "codecov>=2.0.15",
        "coverage>=4.5.4",
        "cryptography>=2.3.1",
        "docutils>=0.15.2",
        "h11>=0.7.0",
        "h2>=3.1.1",
        "hpack>=3.0.0",
        "hyperframe>=5.2.0",
        "idna>=2.8",
        "importlib-metadata>=0.23",
        "kaitaistruct>=0.8",
        "ldap3>=2.5.2",
        "mitmproxy>=4.0.4",
        "more-itertools>=7.2.0",
        "nose>=1.3.7",
        "parse>=1.12.1",
        "parse-type>=0.5.2",
        "passlib>=1.7.1",
        "pkginfo>=1.5.0.1",
        "pluggy>=0.13.0",
        "pyasn1>=0.4.6",
        "pycparser>=2.19",
        "Pygments>=2.4.2",
        "pyOpenSSL>=18.0.0",
        "pyparsing>=2.2.2",
        "pyperclip>=1.6.5",
        "readme-renderer>=24.0",
        "requests>=2.22.0",
        "requests-toolbelt>=0.9.1",
        "ruamel.yaml>=0.15.100",
        "selenium>=3.141.0",
        "six>=1.12.0",
        "sortedcontainers>=2.0.5",
        "tornado>=5.1.1",
        "tqdm>=4.35.0",
        "twine>=1.13.0",
        "urllib3>=1.25.3",
        "urwid>=2.0.1",
        "webencodings>=0.5.1",
        "wsproto>=0.11.0",
        "zipp>=0.6.0"
    ]
)
