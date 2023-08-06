import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="find-min",
    version="2.0.0",
    author="Syed Rafey Husain",
    author_email="rafey.husain@outlook.com",
    description="Find the minimum in array using as few comparisons as possible",
    long_description="Given an array of elements that provide a less than operator, find the minimum using as few comparisons as possible. The array shall be given such that the first few elements are strictly monotonically decreasing, the remaining elements are strictly monotonically increasing. The less than operator be defined as the operator that works on such arrays where a < b if min(a,b) == a.",
    long_description_content_type="text/markdown",
    url="https://github.com/rafey.husain/findMin",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)