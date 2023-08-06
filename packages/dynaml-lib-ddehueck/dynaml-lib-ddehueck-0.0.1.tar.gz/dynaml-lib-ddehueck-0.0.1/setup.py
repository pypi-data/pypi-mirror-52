import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dynaml-lib-ddehueck",
    version="0.0.1",
    author="Cole Morgan, Devin de Hueck, Henry Creamer, Jonathon Cai",
    author_email="d.dehueck@gmail.com",
    description="A research toolkit for understanding how misinformation flows through a social network through dynamic system simulation and graph neural networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ddehueck/dynaml-lib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)