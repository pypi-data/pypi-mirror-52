import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="googleauthentication",
    version="0.0.1",
    author="Dacker",
    author_email="hello@dacker.co",
    description="A meta package to be connected to Google services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dacker-team/googleauthentication",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)