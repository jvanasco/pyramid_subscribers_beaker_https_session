"""pyramid_subscribers_beaker_https_session installation script.
"""
import os

from setuptools import setup
from setuptools import find_packages

try:
    here = os.path.abspath(os.path.dirname(__file__))
    README = open(os.path.join(here, "README.md")).read()
    README = README.split("\n\n", 1)[0] + "\n"
except:
    README = ''

requires = [
    "pyramid",
    "pyramid_beaker",
    "pyramid_https_session_core",
]

setup(
    name="pyramid_subscribers_beaker_https_session",
    author="Jonathan Vanasco",
    author_email="jonathan@findmeon.com",
    url="https://github.com/jvanasco/pyramid_subscribers_beaker_https_session",
    version="0.1.2",
    description="provides for a 'session_https' secure session object",
    keywords="web pyramid beaker",
    license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
    classifiers=[
        "Intended Audience :: Developers",
        "Framework :: Pyramid",
        "Programming Language :: Python",
        "License :: Repoze Public License",
    ],
    long_description=README,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    test_suite="tests",
)
