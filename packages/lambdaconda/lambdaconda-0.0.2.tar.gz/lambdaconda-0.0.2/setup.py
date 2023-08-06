import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lambdaconda",
    version="0.0.2",
    author="Riley Mathews",
    author_email="rileymathews80@gmail.com",
    description="Playing around with an AWS lambda library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rileymathews/lambdaconda",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
