import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jutlautil",
    version="0.0.1",
    author="Amandeep Jutla",
    author_email="ajutla@amandeepjutla.com",
    description="Package for personal utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amandeepjutla/jutlautil",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
