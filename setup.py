"""Setup configuration for mortgage calculator package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mortgage-calculator",
    version="1.0.0",
    author="Keith Morgan",
    author_email="keith.morgan@ucdconnect.ie",
    description="A user-friendly mortgage calculator with visualization and export features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/keith-msc/mortgage-interest-calc-py",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "python-dateutil>=2.8.2",
        "matplotlib>=3.5.0",
    ],
    entry_points={
        "console_scripts": [
            "mortgage-calculator=mortgage_calculator.main:main",
        ],
    },
    package_data={
        "mortgage_calculator": ["py.typed"],
    },
    include_package_data=True,
    zip_safe=False,
)
