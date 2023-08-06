import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asyncprogressor",
    version="0.1.3",
    author="Vlad Nadzuga",
    author_email="nadzuga0vlad@gmail.com    ",
    description="Package for showing progress on your function based on last run",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vnadzuga/asyncprogressor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)