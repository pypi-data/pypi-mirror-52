import setuptools

__version__ = "0.2.0"

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="ems-dataflow-testframework",
    version=__version__,
    author="Emarsys",
    description="Framework helping testing Google Cloud Dataflows",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests", "test_.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
