Deltacompression
================

Installation
============
To run, install all necessary dependencies:
pip install -r requirements.txt
and wxPython (for ubuntu):
apt-get install python-wxgtk2.8

Using virtualevn?
================
If you are using virtualevn you will probably have problem with wxPython.
You should add this library to your virtualenv:

cd <env>/lib/python-2.7/site-packages
ln -s /usr/lib/python2.7/dist-packages/wx-2.8-gtk2-unicode/ .
ln -s /usr/lib/python2.7/dist-packages/wx.pth .
ln -s /usr/lib/python2.7/dist-packages/wxversion.py .
ln -s /usr/lib/python2.7/dist-packages/wxversion.pyc .

Running tests
=============
nosetests --with-coverage

Running application
===================
python deltacompresion/main.py
