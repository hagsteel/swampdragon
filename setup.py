import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="SwampDragon",
    version="0.3.0",
    author="Jonas Hagstedt",
    author_email="hagstedt@gmail.com",
    description=("Swamp dragon is a powerful platform making it easy to build real time web applications, combining the power of Django and Tornado"),
    license="BSD",
    keywords="swamp dragon, realtime, sockjs, django, tornado, framework",
    url="https://github.com/jonashagstedt/swampdragon",
    # packages=[
    #     'swampdragon',
    #     'swampdragon.cache',
    #     'swampdragon.connections',
    #     'swampdragon.management',
    #     'swampdragon.pubsub_providers',
    #     'swampdragon.serializers',
    #     'swampdragon.sessions',
    # ],
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
    ],
)
