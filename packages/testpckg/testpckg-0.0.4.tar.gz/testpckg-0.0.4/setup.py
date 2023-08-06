import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testpckg",
    version="0.0.4",
    author="neha",
    author_email="neha.r.garde@gma.com",
    description="A small test example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nehagarde/testingpckg1",
    packages=setuptools.find_packages(),
)