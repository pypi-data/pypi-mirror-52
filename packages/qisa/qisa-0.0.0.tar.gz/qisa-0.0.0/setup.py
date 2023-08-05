import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qisa",
    version="0.0.0",
    author="Bo Zhao",
    author_email="bo.zhao@leicester.ac.uk",
    description="qISA is an extended ISA data model with enhanced quality assurance layer. This tool provides a command line UI and user-friendly GUI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rcfgroup/qISA",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)