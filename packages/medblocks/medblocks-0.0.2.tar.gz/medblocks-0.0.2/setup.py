import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="medblocks",
    version="0.0.2",
    author="Sidharth R",
    author_email="tornadoalert@gmail.com",
    description="MedBlocks python client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/medblocks/medblocks.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.2',
)
