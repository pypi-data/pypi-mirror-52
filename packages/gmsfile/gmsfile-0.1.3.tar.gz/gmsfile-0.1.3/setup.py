import setuptools

with open("README.md", "r") as fh:
    long_description=fh.read()

setuptools.setup(
        name="gmsfile",
        version="0.1.3",
        author="Gourab Kanti Das",
        author_email="gourabkanti.das@visva-bharati.ac.in",
        description="A converter from XYZ to GAMESS file",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/amardrylab/gmsfile3",
        packages = setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.7',
)
