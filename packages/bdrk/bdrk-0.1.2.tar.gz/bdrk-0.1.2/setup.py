import setuptools
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bdrk",
    version="0.1.2",
    author="basis-ai.com",
    author_email="contact@basis-ai.com",
    description="Client library for Bedrock platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/basisai/span",
    install_requires=["requests", "six"],
    extras_require={
        "cli": ["Click", "docker", "jsonschema", "pyhcl"],
        "fs": ["redis", "fakeredis", "msgpack"],
    },
    packages=find_packages(),
    package_data={"": ["*.hcl", "README.md"]},
    exclude_package_data={"": ["README.md"]},
    classifiers=["Programming Language :: Python :: 3"],
    entry_points={"console_scripts": ["bdrk = bedrock_client.bedrock.main:main [cli]"]},
)
