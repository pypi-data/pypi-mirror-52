import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ts-eval",
    version="0.0.1",
    author="Vladimir Shulyak",
    author_email="vladimir@shulyak.net",
    description="Time Series analysis and evaluation tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vshulyak/ts-eval",
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas>=0.23.0',
        'numpy>=1.16.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
