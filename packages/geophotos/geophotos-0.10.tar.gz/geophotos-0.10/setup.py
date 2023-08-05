import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
     name='geophotos',
     version='0.10',
     author="Jake Brehm",
     author_email="code@jakebrehm.com",
     license='MIT',
     description="A package to pull, plot, and analyze coordinates from phots.",
     long_description=README,
     long_description_content_type="text/markdown",
     url="https://github.com/jakebrehm/geophotos",
     packages=find_packages(),
     package_data={
        '': ['*.shp', '*.shx', '*.dbf', '*.prj']
     },
     install_requires=[
        'pillow',
        'folium',
        'webbrowser',
        'osgeo',
        'fiona',
        'geopandas',
     ],
     include_package_data=True,
     classifiers=[
         "Programming Language :: Python :: 3.7",
         "Operating System :: OS Independent",
     ],
 )
