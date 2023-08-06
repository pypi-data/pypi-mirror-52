from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name="woah",
    version="0.1",
    description = "Wait for reasonable load average",
    long_description = readme,
    long_description_content_type = "text/markdown",
    author = "Tim Hatch",
    author_email = "tim@timhatch.com",
    packages=find_packages(),
    install_requires = ['psutil>=5.6.0'],
    entry_points = {
        "console_scripts": [
            "woah = woah.cmdline:main",
        ],
    },
    url = "https://github.com/thatch/woah",
    python_requires = ">=3.6",
)

