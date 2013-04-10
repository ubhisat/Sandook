# **Sandook**
-------------------


Sandook is a command line task management utility for linux based systems.
It can be run under cygwin on windows.

![Sandook.png](http://dl.dropbox.com/u/153809199/Sandook.png "Sandook Task Manager")

## Requirements
---------------

Sandook requires

+ python 2.7
+ urwid
+ dropbox (required for sync to work!)

## Installation
----------------

+ extract the downloaded sandook-x.x.tar.gz or sandook-x.x.zip file
+ At the command prompt execute:  ```python setup.py install  ```. You may need admin privileges depending upon your setup.
+ run ```sandook```
+ Press ```ctrl+p``` to show a help dialog for a list of available commands


## Configuration for sync with dropbox
-----------------

+ Run ```sandook-config -h``` for a list of available commands.
+ This program requires user to provide the APP_KEY and APP_SECRET which can be acquired by registering an app at (for dropbox, currently supported) [https://www.dropbox.com/developers/apps](https://www.dropbox.com/developers/apps "Create App")
+ Please note that you will have to press ```Enter``` after authorizing the app on your web-browser (which should open automatically) to complete the configuration.

## License
-----------

Sandook is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sandook is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Please see [http://www.gnu.org/licenses/gpl-3.0.html](http://www.gnu.org/licenses/gpl-3.0.html "") for more information.
