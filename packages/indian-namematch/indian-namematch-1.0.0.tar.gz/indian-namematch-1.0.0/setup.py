from setuptools import setup

def readme():
    with open("README.md") as f:
        README = f.read()
    return README

setup(
    name="indian-namematch",
    version="1.0.0",
    description="Indian Fuzzy name Matching Tool.",
    long_description = readme(),
    long_description_content_type = "text/markdown",
    url="https://github.com/siddhesh10/indian-namematch",
    author="Siddhesh Sharma",
    author_email="siddheshatjuit@gmail.com",
    license = 'MIT',    
    packages=["indian_namematch"],
    include_package_data=True,
    install_requires = ["re","nltk","permutations"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
