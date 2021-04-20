import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="inputconsole",
    version="0.0.1",
    author="Nathan Fiscaletti",
    description="A console for Python that will keep all output above the input line without interrupting the input line.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["inputconsole"],
    package_dir={'':'inputconsole/src'},
    install_requires=['readchar']
)