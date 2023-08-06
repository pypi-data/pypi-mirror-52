import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="inky-toolkit-stezante7",
    version="0.1.0",
    author="Stefano Zante",
    author_email="stezante7@gmail.com",
    description="Inky Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stezante7/InkyToolkit-stezante7",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
