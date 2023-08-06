from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="graphub",
    version="0.0.1b",
    description="Simple GraphQL client for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/srinivasreddy/graphub",
    author="Srinivas Reddy Thatiparthy",
    author_email="sr.thatiparthy+python@gmail.com",
    license="MIT",
    packages=["graphub"],
    zip_safe=False,
)
