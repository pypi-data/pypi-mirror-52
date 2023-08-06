import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SMRTBridge",
    version="2.1.5",
    author="SMRT-WSU",
    author_email="",
    description="A work in progress project for running bridge in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SMRT-WSU/cards",
    packages=setuptools.find_packages(),
    license='GPL-3.0',
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)