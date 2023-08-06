import setuptools
import os

INSTALL_REQUIRES = [
    'notebook>=5.5.0',
]

with open("README-Pypi.md", "r") as fh:
    long_description = fh.read()

# Enable the nbextension (like jupyter nbextension enable --sys-prefix)
DATA_FILES = [
    ("share/jupyter/nbextensions/accessibility_toolbar", [
        "accessibility_toolbar/static/main.js",
    ]),
    ("etc/jupyter/nbconfig/notebook.d", [
        "jupyter-config/nbconfig/notebook.d/accessibility_toolbar.json"
    ]),
]

setuptools.setup(
    name="accessibility_toolbar",
    version="1.0.30",
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
    data_files=DATA_FILES,
    install_requires=INSTALL_REQUIRES,
)