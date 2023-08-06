import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="utempid",
    version="1.0.0",
    author="Maxime Schoemans",
    author_email="maxime.schoemans@ulb.ac.be",
    description="Unique temporary id generator for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mschoema/utempid",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)