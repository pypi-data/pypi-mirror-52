import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="appel_geocode",
    version="0.1.2",
    author="Gabriel Coimbra",
    author_email="gcoimbra@riseup.net",
    description="A faster spatial join/reverse geocoding algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gcoimbra/appel",
    packages=setuptools.find_packages(),
    install_requires=[
        'matplotlib==3.1.1',
        'Shapely==1.6.4.post2',
        'geopandas==0.5.1',
        'numpy==1.17.2',
        'pandas==0.25.1',
        'typing-extensions==3.7.4'

    ],

    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
)
