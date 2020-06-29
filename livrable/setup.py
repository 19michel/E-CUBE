import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="project_E-CUBE",
    version="0.0.1",
    author="Léopold Védie Stephen Piet Grégoire Michel",
    author_email="author@example.com",
    description="A project to calculate the electrical consumption of french firms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)