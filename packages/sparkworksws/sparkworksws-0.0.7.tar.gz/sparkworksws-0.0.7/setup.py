import os
from distutils.command.register import register as register_orig
from distutils.command.upload import upload as upload_orig

from setuptools import setup


class register(register_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')


class upload(upload_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')


with open("README.rst", "r") as fh:
    long_description = fh.read()

# from distutils.core import setup
setup(
    name='sparkworksws',
    packages=['sparkworksws'],
    version='0.0.7',
    description='A client library for the sparkworks websocket api',
    long_description=long_description,
    author='SparkWorks ITC',
    author_email='info@sparkwokrs.net',
    url='https://www.sparkworks.net/',  # use the URL to the github repo
    download_url='https://github.com/SparkWorksnet/client',  # I'll explain this in a second
    keywords=['client', 'sparkworks', 'websocket'],  # arbitrary keywords
    include_package_data=True,
    classifiers=[],
    cmdclass={
        'register': register,
        'upload': upload,
    },
    install_requires=['pyOpenSSL', 'service_identity', 'twisted', 'autobahn']
)
