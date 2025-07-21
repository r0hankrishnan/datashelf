from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="datashelf",
    version="0.1.0",
    author="Rohan Krishnan",  
    author_email="your.email@example.com",  
    description="A git-like version control system for datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/r0hankrishnan/datashelf",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Version Control",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.0.0",
        "pyyaml>=5.0.0",
        "numpy>=1.18.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "datashelf=datashelf.core:main",  # Optional CLI entry point
        ],
    },
)