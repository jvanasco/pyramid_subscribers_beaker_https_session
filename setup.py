"""pyramid_subscribers_beaker_https_session installation script.
"""
import os

from setuptools import setup
from setuptools import find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
long_description = description = "provides for a 'session_https' secure session object"
with open(os.path.join(HERE, "README.md")) as fp:
    long_description = fp.read()

requires = [
    "pyramid",
    "pyramid_beaker",
    "pyramid_https_session_core",
]
tests_require = ["pytest"]
testing_extras = tests_require + []


setup(
    name="pyramid_subscribers_beaker_https_session",
    author="Jonathan Vanasco",
    author_email="jonathan@findmeon.com",
    url="https://github.com/jvanasco/pyramid_subscribers_beaker_https_session",
    version="0.1.2",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="web pyramid beaker",
    license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
    classifiers=[
        "Intended Audience :: Developers",
        "Framework :: Pyramid",
        "Programming Language :: Python",
        "License :: Repoze Public License",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        "testing": testing_extras,
    },
    test_suite="tests",
)
