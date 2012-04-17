"""pyramid_subscribers_beaker_https_session installation script.
"""
import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.txt")).read()
README = README.split("\n\n", 1)[0] + "\n"

requires = [
    "pyramid",
    "pyramid_beaker"
    ]

setup(name="pyramid_subscribers_beaker_https_session",
      version="0.0.3",
      description="provides for a 'session_https' secure session object",
      long_description=README,
      classifiers=[
        "Intended Audience :: Developers",
        "Framework :: Pyramid",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        ],
      keywords="web pyramid beaker",
      py_modules=['pyramid_subscribers_beaker_https_session'],
      author="Jonathan Vanasco",
      author_email="jonathan@findmeon.com",
      url="https://github.com/jvanasco/pyramid_subscribers_beaker_https_session",
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      tests_require = requires,
      install_requires = requires,
      test_suite='tests',
      )

