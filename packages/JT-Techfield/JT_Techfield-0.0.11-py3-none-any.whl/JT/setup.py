import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JT",
    version="0.0.2",
    author="Jacob Thompson",
    author_email="jacob.thompson@techfield.us",
    description="My regression module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
)