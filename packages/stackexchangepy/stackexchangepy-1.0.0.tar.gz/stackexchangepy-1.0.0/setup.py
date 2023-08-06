from setuptools import setup
from os import path

current_path = path.abspath(path.dirname(__file__))
with open(path.join(current_path, 'README.rst'), encoding='utf-8') as file:
      long_description = file.read()

print(long_description)

setup(
    name='stackexchangepy',
    version='1.0.0',
    description='StackExchangePy API Wrapper',
    long_description=long_description,
    url='https://github.com/monzita/stackexchangepy',
    author='Monika Ilieva',
    author_email='hidden@hidden.com',
    packages=['stackexchangepy', 'stackexchangepy.module', 'stackexchangepy.network'],
    package_dir={'stackexchangepy': 'stackexchangepy'},
    install_requires = ['requests', 'tinynetrc', 'arrow'],
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
      'Programming Language :: Python :: 3.6'
    ],
    license='GNU General Public License v3 or later (GPLv3+)',
    keywords='stackexchangepy api wrapper python3',
)