import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="matfin",
    version="0.0.2",
    author="Felipe Bailez",
    author_email="bailez@usp.br",
    description="Simple package with mathematical finance functions for me to use in my finance course at the Univeristy of São Paulo. :)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bailez/matfin   ",
    packages=setuptools.find_packages(),
    license='MIT',
    python_requires='>=3.7',
) 
