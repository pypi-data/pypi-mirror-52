import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyjlib",
    version="0.0.1",
    author="Mohammad Abouali",
    author_email="maboualidev@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maboualidev/PyJLib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)
