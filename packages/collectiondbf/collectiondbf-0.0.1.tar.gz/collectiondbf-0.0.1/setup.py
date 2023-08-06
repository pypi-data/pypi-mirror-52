import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="collectiondbf",
    version="0.0.1",
    author="Jesse Khorasanee",
    author_email="jessekhorasanee@gmail.com",
    description="Download all files in a Blackfynn collection via command line or gui",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
    ],
    install_requires=[
         'blackfynn',
         'requests'
    ],
    python_requires='>=3.6',
)