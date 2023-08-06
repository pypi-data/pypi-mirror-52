import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="handymodules",
    version="2.0.1",
    author="Adam Wasilewski",
    author_email="adam@wasilewski.pw",
    description="A few handy, useful python modules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/handymodules/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
