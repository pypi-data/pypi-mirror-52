import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aprioripy",
    version="0.0.2",
    author="Gökhan Gerdan",
    author_email="gokhang1327@gmail.com",
    description="Apriori algorithm.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gokhangerdan/Aprioripy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)