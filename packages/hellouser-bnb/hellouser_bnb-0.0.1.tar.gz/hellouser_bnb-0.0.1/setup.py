import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hellouser_bnb",
    version="0.0.1",
    author="Bhushan",
    author_email="bhushan.bhupta@accenture.com",
    description="Hello User Module",
    package_dir={"":"src"},
    long_description=long_description,
    long_description_type="text/markdown",
    py_modules=["hello"],
    
)