import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="heartpy",
    version="1.2.2",
    author="Paul van Gent",
    author_email="P.vanGent@tudelft.nl",
    description="Heart Rate Analysis Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paulvangentcom/heartrate_analysis_python",
    packages=["heartpy"],
    install_requires=["numpy", "scipy", "matplotlib"],
    include_package_data=True,
    package_data={
        '': ['data/*.csv', 'data/*.mat', 'data/*.log']       
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
)
