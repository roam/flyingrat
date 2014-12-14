import os
from setuptools import setup

def read(*paths):
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='flyingrat',
    version='0.1.0',
    description='Simple mail server for local development',
    long_description=read('README.rst'),
    url='https://github.com/roam/flyingrat/',
    author='Kevin Wetzels',
    author_email='kevin@roam.be',
    license='BSD',
    packages=['flyingrat'],
    include_package_data=True,
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        flyingrat=flyingrat.cli:cli
    ''',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
