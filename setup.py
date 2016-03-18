import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="SwampDragon",
    version="0.4.2.2",
    author="Jonas Hagstedt",
    author_email="hagstedt@gmail.com",
    description=("SwampDragon is a powerful platform making it easy to build real time web applications, combining the power of Django and Tornado"),
    license="BSD",
    keywords="SwampDragon, websockets, realtime, sockjs, django, tornado, framework",
    url="http://swampdragon.net",
    packages=find_packages(),
    long_description=read('README.txt'),
    include_package_data=True,
    entry_points={'console_scripts': ['dragon-admin = swampdragon.core:run', ]},
    install_requires=[
        "Django>=1.6,<1.10",
        "Tornado >= 3.2.2",
        "sockjs-tornado >= 1.0.0",
        "tornado-redis >= 2.4.18",
        "redis >= 2.8",
        "python-dateutil >= 2.2"
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
