# SwampDragon


[![Downloads](https://pypip.in/download/SwampDragon/badge.svg?style=flat&?period=month)](https://pypi.python.org/pypi/SwampDragon/)
[![PyVersion](https://pypip.in/py_versions/SwampDragon/badge.svg?style=flat&)](https://pypi.python.org/pypi/SwampDragon/)

![](https://codeship.com/projects/fcebb9f0-1270-0132-b84c-7ee8f6cd4d2b/status?branch=master)

Build real-time web applications with Django.

Features:

*  Real-time data
*  Self publishing model
*  Make use of the wonderful features of Django
*  Serializers handling Django models
*  Customisable field serializers
*  Routers that are easy to understand
*  Angular JS support
*  Query style data subscriptions
*  Easy to implement in existing Django projects


SwampDragon makes use of Djangos wonderful ORM, Tornados excellent websocket support (with fallback. Tested in IE7), and
Redis blazing speed.

## Installation

    pip install swampdragon
    
**note:** Redis 2.8 or higher required
    
   
## Quickstart

See [documentation](http://swampdragon.net/documentation/) and example projects in this repository.

[Tutorial](http://swampdragon.net/tutorial/part-1-here-be-dragons-and-thats-a-good-thing/) available here.

# Documentation

See [Documentation](http://swampdragon.net/documentation/) here


# Changelog

See change logs at [swampdragon.net](http://swampdragon.net/changelog/) here


# Contributing and running the tests

Feel free to make a pull request, just make sure you write tests to cover the changes / additions you make.

To run the tests install Tox and run `tox` (in the same directory as tox.ini)


# License

Copyright (c) 2014, jonas hagstedt 
All rights reserved. 

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met: 

 * Redistributions of source code must retain the above copyright notice, 
   this list of conditions and the following disclaimer. 
 * Redistributions in binary form must reproduce the above copyright 
   notice, this list of conditions and the following disclaimer in the 
   documentation and/or other materials provided with the distribution. 
 * Neither the name of  nor the names of its contributors may be used to 
   endorse or promote products derived from this software without specific 
   prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE. 
