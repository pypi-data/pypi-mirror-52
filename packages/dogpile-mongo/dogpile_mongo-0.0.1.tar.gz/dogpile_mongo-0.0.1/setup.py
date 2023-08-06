import os
import re
import sys

from setuptools import setup, find_packages


v = open(
    os.path.join(
        os.path.dirname(__file__),
        'dogpile_mongo', '__init__.py')
)
VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)
v.close()

readme = os.path.join(os.path.dirname(__file__), 'README.rst')

setup(
    name='dogpile_mongo',
    version=VERSION,
    description="backend for dogpile.cache with reading and writing on mongodb",
    long_description=open(readme).read(),
    install_requires=['dogpile.cache>=0.6.2', 'pymongo'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    keywords='caching',
    author='Massimo Cavalleri',
    author_email='submax@tiscali.it',
    url='https://bitbucket.org/submax82/dogpile_mongo',
    license='MIT',
    packages=find_packages(),
    entry_points="""
    [dogpile.cache]
    mongo = dogpile_mongo.backends:MongoBackend
    """,
    zip_safe=True,
)
