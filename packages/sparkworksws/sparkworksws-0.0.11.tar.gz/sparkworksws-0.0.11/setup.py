import os
from distutils.command.register import register as register_orig
from distutils.command.upload import upload as upload_orig

from setuptools import setup

NAME = 'sparkworksws'
PACKAGES = ['sparkworksws']
VERSION = '0.0.11'
DESCRIPTION = 'A client library for the sparkworks websocket api'
REQUIRED_PACKAGES = ['pyOpenSSL', 'service_identity', 'twisted', 'autobahn', 'sparkworksrest']


class register(register_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')


class upload(upload_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')


with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    packages=PACKAGES,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    author='SparkWorks ITC',
    author_email='info@sparkwokrs.net',
    url='https://www.sparkworks.net/',  # use the URL to the github repo
    download_url='https://github.com/SparkWorksnet/client',  # I'll explain this in a second
    keywords=['client', 'sparkworks', 'websocket'],  # arbitrary keywords
    include_package_data=True,
    classifiers=[],
    install_requires=REQUIRED_PACKAGES,
    cmdclass={
        'register': register,
        'upload': upload,
    }
)
