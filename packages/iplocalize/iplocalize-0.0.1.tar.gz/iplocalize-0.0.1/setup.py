import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iplocalize",
    version="0.0.1",
    author="Yoann Lamouroux",
    author_email="ylamouroux@ubuntu.com",
    description="Localize and test a given freeproxy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ylmrx/iplocalize",
    packages=setuptools.find_packages(),

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'geoip2',
        'pygments'
    ],
    entry_points = {
        'console_scripts': ['iplocalize=iplocalize.cmd:main'],
    }
)

