from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()
VERSION = '0.0.6'

setup(
    name='dotGraph_Rhy',
    version=VERSION,
    description='easily draw a picture by using graphviz',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='draw picture!',
    author='RhythmLian',
    author_mail='RhythmLian@outlook.com',
    url="https://github.com/Rhythmicc/dotGraph",
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'dotGraph = dotGraph.main:main'
        ]
    },
)
