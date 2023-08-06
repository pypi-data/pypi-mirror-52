import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pmxutils",
    version="0.0.3",
    author="Stefan Mack",
    author_email="stefan_mack@hotmail.com",
    description="Collection of tools for programmation and modeling X",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Areskiko/stefan-tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)