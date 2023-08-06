import os
from setuptools import setup

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(BASE_DIR, 'README.md')).read()

setup(
    name='dj-paystack',
    version='0.1',
    packages=['dj_paystack'],
    description='Paystack for Django',
    long_description=README,
    author='ebinabo',
    author_email='edgarjohn95@gmail.com',
    url='https://github.com/ebinabo/dj-paystack/',
    license='MIT',
    install_requires=[
        'Django>=2.0',
    ]
)