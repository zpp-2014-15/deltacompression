Deltacompression
================

Installation
============
To run, install all necessary dependencies:
````bash
pip install -r requirements.txt
apt-get install python-wxgtk2.8
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
in repository (directory that contains README.md etc)

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

