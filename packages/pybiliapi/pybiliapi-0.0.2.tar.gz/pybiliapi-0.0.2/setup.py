from setuptools import setup, find_packages

setup(
    name = "pybiliapi",
    version = "0.0.2",
    keywords = ("bilibili", "api", "bunnyxt"),
    description = "A python package for bilibili api call.",
    long_description = "A python package for bilibili api call.",
    license = "GNU General Public License v3.0 ",

    url = "https://github.com/bunnyxt/pybiliapi",
    author = "bunnyxt",
    author_email = "bunnyxt@outlook.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['urllib3']
)