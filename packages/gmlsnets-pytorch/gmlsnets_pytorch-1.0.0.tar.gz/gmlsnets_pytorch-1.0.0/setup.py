import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gmlsnets_pytorch",
    version="1.0.0",
    author="Ben J. Gross and Paul J. Atzberger",
    author_email="atzberg@gmail.com",
    description="Implementation of GMLS-Nets in PyTorch.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://atzberger.org/",
    packages=setuptools.find_packages(include=['gmlsnets_pytorch']),
    #setup_requires=["numpy>=1.16","scipy>=1.3","matplotlib>=3.0"],
    #install_requires=["numpy>=1.16","scipy>=1.3","matplotlib>=3.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

