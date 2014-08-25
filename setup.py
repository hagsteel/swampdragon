import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="SwampDragon",
    version="0.3.5.1",
    author="Jonas Hagstedt",
    author_email="hagstedt@gmail.com",
    description=("SwampDragon is a powerful platform making it easy to build real time web applications, combining the power of Django and Tornado"),
    license="BSD",
    keywords="SwampDragon, realtime, sockjs, django, tornado, framework",
    url="http://swampdragon.net",
    packages=find_packages(),
    long_description=read('README.md'),
    include_package_data=True,
    entry_points={'console_scripts': ['dragon-admin = swampdragon.core:run',]},
    install_requires=[
        "Django >= 1.4",
        "Tornado",
        "sockjs-tornado",
        "tornado-redis",
        "redis",
        "python-dateutil"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
)
