import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pigUI",
    version="0.0.0",
    author="s0lst1ce",
    author_mail="thithib.cohergne@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/s0lst1ce/pigUI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0 License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7")
