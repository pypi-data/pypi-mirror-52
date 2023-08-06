import setuptools

with open("README-Pypi.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="accessibility_toolbar",
    version="1.0.14",
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