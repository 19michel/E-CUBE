import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ecube_conso",
    version="0.0.1",
    author="Leopold Vedie / Stephen Piet / Gregoire Michel",
    description="A project to calculate the electrical consumption of french firms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/19michel/E-CUBE.git",
    packages=['project'],
    classifiers=[
    "Natural Language :: French"
    "Programming Language :: Python :: 2.7"
    ],
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'shapely',
        'pyshp',
        'pyproj',
        'simpledbf',
        'scipy'
    ],
    python_requires='>=3.6',
)