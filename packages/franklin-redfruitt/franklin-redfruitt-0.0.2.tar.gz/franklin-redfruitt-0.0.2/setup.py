import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="franklin-redfruitt",
    version="0.0.2",
    author="redfruitt",
    author_email="krishnaqmar@gmail.com",
    description="Franklin Book Recommendations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/redfruitt/Franklin",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)