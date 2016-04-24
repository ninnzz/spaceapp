from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='AirVironment',
    version='1.0',
    long_description=read('README.md'),
    packages=['app', 'data', 'instance', 'lib', 'util'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'mutagen',
        'sqlalchemy',
        'pymysql',
        'requests',
        'uwsgi',
        'flask-cors',
        'Flask-Mail',
        'Flask'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ]
)
