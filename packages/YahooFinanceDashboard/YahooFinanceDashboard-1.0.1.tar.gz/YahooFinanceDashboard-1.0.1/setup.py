import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="YahooFinanceDashboard",
    version="1.0.1",
    author="Daniel Moseguí González",
    author_email="d.mosegui@gmail.com",
    description="API for accessing, synchronizing, managing locally and plotting Yahoo financial data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mosegui/YahooFinanceDashboard",
    license='BSD3',
    packages=setuptools.find_packages(),
    install_requires=[
        "yahoofinancials",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)