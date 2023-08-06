from setuptools import find_packages, setup

with open("README.md") as f:
    readme = f.read()

with open("requirements-dev.txt") as f:
    requires = f.read().strip().splitlines()

setup(
    name="woah",
    version="0.2",
    description="Wait for reasonable load average",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Tim Hatch",
    author_email="tim@timhatch.com",
    url="https://github.com/thatch/woah",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
    license="Apache 2.0",
    packages=find_packages(),
    test_suite="woah.tests",
    test_requires=requires,
    python_requires=">=3.6",
    entry_points={"console_scripts": ["woah = woah.cmdline:main"]},
)
