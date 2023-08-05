import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ifsFractals",
    version="0.0.2",
    author="Peter Francis",
    author_email="franpe02@gettysburg.edu",
    description="For Generating Fast IFS Fractals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/francisp336/IFSFGl",
    py_modules=["ifsFractals"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # python_requires='>=3.7.3',
    install_requires=['imageio', 'matplotlib', 'numba', 'numpy', 'Pillow', 'scipy', 'system', 'termcolor', 'typing'],
    keywords='sample setuptools development'
)
