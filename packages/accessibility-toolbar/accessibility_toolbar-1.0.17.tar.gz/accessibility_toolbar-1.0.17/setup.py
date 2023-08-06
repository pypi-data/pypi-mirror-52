import setuptools
import os

INSTALL_REQUIRES = [
    'notebook>=5.5.0',
]

with open("README-Pypi.md", "r") as fh:
    long_description = fh.read()


nbext = ["share", "jupyter", "nbextensions"]
for (path, dirs, files) in os.walk(os.path.join("rise", "static")):
    # Files to install
    srcfiles = [os.path.join(path, f) for f in files]
    # Installation path components, removing rise/static from "path"
    dst = nbext + path.split(os.sep)[2:]
    DATA_FILES.append((os.path.join(*dst), srcfiles))

setuptools.setup(
    name="accessibility_toolbar",
    version="1.0.17",
    author="MSJUPYTER",
    author_email="joshua.zeltser@gmail.com",
    description="An Accessibility Toolbar for Jupyter Notebooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/uclixnjupyternbaccessibility/accessibility_toolbar",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)