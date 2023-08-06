import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
    name="pyfcomb",
    version="1.0.7",
    author="Marco Müllner",
    author_email="muellnermarco@gmail.com",
    description="Computing frequency combinations made simple",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarcoMuellner/pyfcomb",
    install_requires=requirements,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
