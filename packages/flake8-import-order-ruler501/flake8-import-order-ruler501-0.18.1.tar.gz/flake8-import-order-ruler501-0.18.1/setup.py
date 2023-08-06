# coding: utf-8
import os

from setuptools import setup


def readme():
    path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(path, 'README.md'), 'rU', encoding='utf-8') as f:
        return f.read()


setup(
    name="flake8-import-order-ruler501",
    version="0.18.1",
    author="ruler501",
    author_email="ruler501@ruler501.com",
    description="ruler501's flake8-import-order plugin.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="flake8-import-order ruler501",
    license="MIT",
    url="https://github.com/ruler501/flake8-import-order-ruler501",
    packages=["flake8_import_order_ruler501"],
    python_requires=">=3.4",
    install_requires=["flake8-import-order>=0.18"],
    entry_points={
        "flake8_import_order.styles": [
            "ruler501 = flake8_import_order_ruler501:Ruler501ImportOrderStyle"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Flake8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)