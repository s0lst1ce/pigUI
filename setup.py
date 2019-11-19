import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pigUI",
    version="1.0.4-alpha",
    author="s0lst1ce",
    author_mail="thithib.cohergne@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/s0lst1ce/pigUI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["pygame>=2.0.0.dev3"])
