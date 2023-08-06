from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='petrovna',
    version='1.0.2',
    description='Validatee bic, inn, kpp, ogrn, ogrnip, corr. account, account number, snils',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://example.com',
    author='KODE LLC',
    platforms='Any',
    packages=find_packages(exclude=('tests',)),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
    zip_safe=False
)
