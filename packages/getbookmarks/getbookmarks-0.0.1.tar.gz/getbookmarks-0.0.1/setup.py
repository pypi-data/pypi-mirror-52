import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="getbookmarks",
    version="0.0.1",
    author="Victor Coelho",
    author_email="victorhdcoelho@gmail.com",
    description="Get bookmarks from pdf.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/gpam/services/getbookmarks",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "PyPDF2"
    ],
)
