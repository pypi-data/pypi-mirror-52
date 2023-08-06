import codecs
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def long_desc(root_path):
    filepath = os.path.realpath(os.path.join(root_path, 'README.rst'))
    with codecs.open(filepath, mode='r') as f:
        return f.read()


setup(
    name="zabana-travis-ci-test",
    description="A Python package to test the Travis-CI PyPI deploy.",
    long_description=long_desc(here),
    license="MIT license",
    author="Karim C",
    author_email="jannis@leidel.info",
    url="https://github.com/zabanaa/travis-ci-pypi-deploy-test",
    version='0.1.1',
    py_modules=['travis_ci_pypi_deploy_test'],
)
