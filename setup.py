from setuptools import setup, find_packages

setup(
    name="safe-pfl-plotter",
    version="0.1.0",
    description="safe-pfl plotter",
    url="https://github.com/safe-pfl/plotters",
    author="MohammadMojtaba Roshani",
    author_email="mohammadmojtabaroshani@outlook.com",
    license="Apache Software License",
    packages=find_packages(),
    install_requires=[
        "torch>=2.5",
        "matplotlib==3.6.3",
        "matplotlib-inline==0.1.7",
        "matplotlib2tikz==0.7.6",
        "scipy>=1.14",
        "scikit-learn>=1.5",
        "numpy>=2.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
)
