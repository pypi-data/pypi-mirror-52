import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Credentials_Validator",
    version="0.0.3",
    author="Leone Bacciu",
    author_email="leonebacciu@gmail.com",
    description="Credential validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LeoneBacciu/Credentials_Validator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
