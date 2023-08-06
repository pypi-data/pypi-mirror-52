from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()
 
setup(
    name="Comickaze",
    version="1.1",
    description="A simple CLI tool where you can download comics easily",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Chr1st-oo",
    author_email="aaroncgonzales.dev@gmail.com",
    packages=find_packages(),
    install_requires=[
        "Click",
        "bs4",
        "requests",
        "tabulate",
        "tqdm",
        "img2pdf"
    ],
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    entry_points='''
        [console_scripts]
        comickaze=comickaze.cli:cli
    '''
)