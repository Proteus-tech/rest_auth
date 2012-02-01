#!/usr/bin/env python

"""
  To create a package, svn export from the tag version you would like to create the package from to
  a folder named django_logger next to this setup.py file and change the version below to be the new version
  Then, to build an egg, type the following command:

  ::

    python setup.py bdist_egg

  Then, create the tar.gz file (please chang the name of the file to your version):

  ::

    tar -cvzf django_logger-0.1-py2.6.tar.gz *


  Don't forget to add the .tar.gz file to svn at https://zeppelin.proteus-tech.com/repos/projects/logger/packages

"""

from setuptools import setup

setup(
    name='rest-auth',
    version='0.2.2',
    description='Classes for helping in authentication between services',
    author='Proteus Technologies Co. Ltd.',
    author_email='team@proteus-tech.com',
    url='https://github.com/Proteus-tech/rest_auth',
    packages=['rest_auth','rest_auth.templatetags'],
    install_requires = ['Django>=1.3.1',],
    dependency_links = [
        'http://github.com/Felspar/django-fost-authn/tarball/master#egg=django-fost-authn',
    ],
)
