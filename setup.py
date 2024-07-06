from setuptools import setup, find_packages

setup(
    name="ACBF",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "cryptography",
        "web3",
        "solcx",
        "flask",
        "flask-restful",
        "pytest",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "aes_encryption=cryptography.symmetric.aes_encryption:main",
            "rsa_encryption=cryptography.asymmetric.rsa_encryption:main",
            "deploy_contract=blockchain.interaction.deploy_contract:main",
            "interact_contract=blockchain.interaction.interact_contract:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="An advanced framework for cryptographic techniques and blockchain interactions",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ACBF",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
