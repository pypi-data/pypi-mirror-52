import os
import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ptscore",
    version="0.1.7",
    author="Caesar Kabalan",
    author_email="caesar.kabalan@gmail.com",
    description="PassTheSecret core library containing back-end code for encryption and storage of secrets.",
    long_description=long_description,
    url="https://github.com/passthesecret/passthesecret-core",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'asn1crypto==0.24.0',
        'boto3==1.9.225',
        'botocore==1.12.225',
        'cffi==1.12.3',
        'cryptography==2.7',
        'docutils==0.15.2',
        'jmespath==0.9.4',
        'pycparser==2.19',
        'python-dateutil==2.8.0',
        's3transfer==0.2.1',
        'six==1.12.0',
        'urllib3==1.25.3'
    ]
)
