import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="api-utils",
    version="2019.9.18",
    description="API utils simplify life when creating or consuming APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/api-utils/",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
