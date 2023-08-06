import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="teslaclient",
    version="0.0.5",
    author="Jeff Shurak",
    author_email="jshurak@gmail.com",
    description="Python Tesla API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jshurak/tesla_client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)