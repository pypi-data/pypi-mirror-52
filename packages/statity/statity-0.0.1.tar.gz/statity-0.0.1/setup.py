import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='statity',
    version="0.0.1",
    author='Andrey Suglobov',
    author_email='sooglobov@gmail.com',
    description='Lib for checking types of functions arguments and returning data to accordance with annotating',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/soogly/pystatity',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)