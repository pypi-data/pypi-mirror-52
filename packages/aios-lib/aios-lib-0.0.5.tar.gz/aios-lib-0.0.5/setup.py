import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aios-lib",
    version="0.0.5",
    author="Zhang Manni",
    author_email="mandy.zhang@clustar.ai",
    description="aios lib package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.clustarai.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python ",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests==2.22.0",
        "requests-unixsocket==0.1.5",
        "jsonpatch==1.16",
        "jsonpointer==1.10",
        "jsonschema==2.6.0",
    ],
)

