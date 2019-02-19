import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
requires = [
    'requests', 'jsonpickle'
    ]
setuptools.setup(
    name="json-store-client",
    version="0.0.1b1",
    author="leon332157",
    author_email="leon332157@gmail.com",
    description="A client library for jsonstore",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leon332157/json-store-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6", "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent", "Topic :: Internet"
        ], install_requires=requires,
    )
