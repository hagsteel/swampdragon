# SwampDragon

# Looking for someone to take over

I no longer have time to support this project, so I am looking for someone to take over.
Please raise an issue in the issue tracker if you are interested in taking over the maintenance of SwampDragon.


## Help needed, and the future of SwampDragon

SwampDragon has a lot of dependencies, and is heavily dependent on Django.
One of the libs that SwampDragon is dependant on is [https://github.com/leporo/tornado-redis](https://github.com/leporo/tornado-redis), and this project looks like it might no longer be maintained (I believe Leporo has done a great job with this library and I understand that he may no longer have time to maintain it)
Going forward I have decided that this needs a solution.

So the current plan for SwampDragon is this:

*  Remove as many external dependencies as possible
*  Make it work with other frameworks like Flask etc. (i.e remove Django as a required dependency)
*  Better testing 
*  More code coverage
*  Swappable serializer (it should be possible to use 3rd party serializers like that of DRF)
*  SelfPublishModel needs rewriting and should be a separate module
*  ... and much more
*  Proper contribution guidelines
  
### How to get there

This is a big job and help is required to get there.
Anything from writing code and tests to reviewing PRs etc. would be appreciated.

If you are interested in helping out let me know.

General conversations about this can be found here: [https://github.com/jonashagstedt/swampdragon/issues/161](https://github.com/jonashagstedt/swampdragon/issues/161)

---

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
