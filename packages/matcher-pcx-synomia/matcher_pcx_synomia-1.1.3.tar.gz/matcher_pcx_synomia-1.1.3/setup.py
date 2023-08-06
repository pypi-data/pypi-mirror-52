import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="matcher_pcx_synomia",
    version="1.1.3",
    author="Synomia",
    author_email="pypi@synomia.com",
    description="Extract themes from verbatims",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
