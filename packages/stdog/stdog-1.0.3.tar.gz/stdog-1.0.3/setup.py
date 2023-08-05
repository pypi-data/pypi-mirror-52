from setuptools import setup, find_packages


with open("README.md", "r") as f:
    README_TEXT = f.read()

setup(
    name="stdog",
    version="v1.0.3",
    packages=find_packages(exclude=["build", ]),
    long_description=README_TEXT,
    long_description_content_type="text/markdown",
    install_requires=["tensorflow", "scipy", "numpy", "emate"],
    include_package_data=True,
    license="MIT",
    description="Structure and Dynamics on Graphs",
    author_email="messias.physics@gmail.com",
    author="Bruno Messias; Thomas K. Peron",
    download_url="https://github.com/stdogpkg/stdog/archive/v1.0.3.tar.gz", 
    keywords=[
        "gpu", "science", "complex-networks", "graphs", "dynamics",
         "tensorflow", "kuramoto"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Information Analysis"
    ],
    url="https://github.com/stdogpkg/stdog"
)
