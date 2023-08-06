import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mbhupdater",
    version="0.1.0",
    author="Adam Thompson-Sharpe",
    author_email="adamthompsonsharpe@gmail.com",
    description="An easy-to-use, OS-Independent updater for games/programs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Unlicense",
    url="https://github.com/MysteryBlokHed/mbhupdater",
    packages=setuptools.find_packages(),
    install_requires=[
        "tqdm"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: Public Domain",
        "Operating System :: OS Independent"
    ]
)