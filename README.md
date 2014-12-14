Deltacompression
================

Installation
============
To run, install all necessary dependencies:
````bash
pip install -r requirements.txt
apt-get install python-wxgtk2.8 python-tk python-matplotlib
````
Moreover, you have to download an xdelta3 package from
[here](https://code.google.com/p/xdelta/downloads/detail?name=xdelta3.0z.tar.gz&can=2&q=).
After checking sha and unpacking, change version of python in the Makefile,
add -fPIC at the end of line 202 in Makefile and run:

````bash
make xdelta3module.so
````

Using virtualenv?
================
If you are using virtualevn you will probably have problem with wxPython.
You should add this library to your virtualenv:
````bash
cd <env>/lib/python-2.7/site-packages
ln -s /usr/lib/python2.7/dist-packages/wx-2.8-gtk2-unicode/ .
ln -s /usr/lib/python2.7/dist-packages/wx.pth .
ln -s /usr/lib/python2.7/dist-packages/wxversion.py .
ln -s /usr/lib/python2.7/dist-packages/wxversion.pyc .
````
PYTHONPATH
==========
Add repository directory to PYTHONPATH
If yo are using virtualenvwrapper just simply type:
````bash
add2virtualenv .
````
in repository (directory that contains README.md etc).

You should also add to PYTHONPATH the directory with xdelta3module.so.

Running tests
=============
````bash
nosetests --with-coverage
````
Testing code style
==================
````bash
pylint deltacompression/
````
Running application
===================
````bash
python deltacompresion/main.py
````

