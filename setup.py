from setuptools import setup, find_packages
from pathlib import Path

root = Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (root / "README.rst").read_text(encoding="utf-8")

setup(
    name="pycollisiondb",
    version="0.1.5",
    description="A package for interacting with CollisionDB",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/xnx/pycollisiondb",
    author="Christian Hill",
    author_email="ch.hill@iaea.org",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
    ],
    keywords="chemistry, formula, species, state, reaction",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "pyvalem>=2.5.10",
        "requests>=2.27.1",
        "numpy>=1.23.1",
        "matplotlib>=3.5.2",
        "pyqn>=1.3.1",
    ],
    extras_require={"dev": ["black", "pytest-cov", "tox", "ipython", "jupyter"]},
    project_urls={
        "Bug Reports": "https://github.com/xnx/pycollisiondb/issues",
    },
)
