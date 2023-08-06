import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='turoboro',
    version='0.0.3',
    scripts=[],
    author="Jon Nylander",
    author_email="pellepim@gmail.com",
    description="A python library for specifying recurring time rules and getting timestamps in return.",
    install_requires=['voluptuous'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pellepim/turoboro",
    packages=['turoboro'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
