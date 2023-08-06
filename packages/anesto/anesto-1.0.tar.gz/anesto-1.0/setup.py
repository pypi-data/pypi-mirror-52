import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anesto",
    version="1.0",
    author="Vitaly Zuevsky",
    author_email="vitaly.zuevsky@gmail.com",
    description="Akamai NetStorage API for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/psvz/anesto",
    py_modules = ["anesto"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests>=2.21.0",
    ],
    python_requires='>=3.6',
)
