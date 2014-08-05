import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="SwampDragon",
    version="0.3.0",
    author="Jonas Hagstedt",
    author_email="hagstedt@gmail.com",
    description=("Swamp dragon is a powerful platform making it easy to build real time web applications, combining the power of Django and Tornado"),
    license="BSD",
    keywords="socketjs pubsub",
    url = "https://github.com/jonashagstedt/swampdragon",
    packages=['swampdragon', ],
    long_description=read('README.md'),
    install_requires=[
        "Django >= 1.4",
        "Tornado",
        "sockjs-tornado",
        "tornado-redis",
        "redis",
        "python-dateutil"
    ],
    classifiers=[
        "Development Status :: Beta",
        "Topic :: WebSocket framework",
        "License :: OSI Approved :: BSD License",
    ],
)
