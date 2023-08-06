import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "RenfeTime",
    version = "0.1.0",
    author = "Ramón Vila Ferreres",
    author_email = "ramon.vila@the-cocktail.com",
    description = "Simple package to obtain and parse train schedules from RENFE",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rmon-vfer/RenfeTime",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)