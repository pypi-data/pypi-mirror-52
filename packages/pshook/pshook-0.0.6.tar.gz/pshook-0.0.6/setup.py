import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pshook",
    version="0.0.6",
    author="Jakob Simon-Gaarde",
    author_email="jakobsg@simon-gaarde.dk",
    description="A small tool that enables monitoring of executable files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/jakobsg/ladon",
    packages=setuptools.find_packages(),
    requires = [
        'psutil'
    ],
    install_requires = [
        'psutil'
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.6',
)
