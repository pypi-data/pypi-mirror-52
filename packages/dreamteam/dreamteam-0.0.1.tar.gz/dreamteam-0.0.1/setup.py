import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dreamteam",
    version="0.0.1",
    author="Dream-Team",
    author_email="abhinav.arora@queensu.ca",
    description="Automated package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moezali1/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)