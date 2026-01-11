from setuptools import setup, find_packages

setup(
    name="ACBF",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "acbf=acbf.cli:main",
            "acbf-api=acbf.api:main",
        ],
    },
    author="ACBF Maintainers",
    author_email="maintainers@example.com",
    description="An educational framework for cryptography and blockchain simulations",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ACBF",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
