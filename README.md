=====================
Installing
=====================

Prerequisites for Developer Machines
====================================

* python 2.7 (install from http://www.ninite.com/ )

(Quick) Setup
=============

* Fork the repo and clone it to your computer using hg clone
* cd into the cloned project
* You will need virtualenv.  Either install it or download virtualenv.py
  from here: https://raw.github.com/pypa/virtualenv/master/virtualenv.py
* Now create a virtualenv.  Use either::

      virtualenv .

  Or::

    python virtualenv.py .

* Good! to activate the env use this on OSX or linux::

    source bin/activate

  On windows::

    Scripts\activate

* Your prompt should start with `(boaz_scrape)`.

* Now install all other requirements (This can take some time)::

    pip install -r requirements.txt

* create folder "xls".

Running the app
=============================
* python scrapit.py [argument]::

    argument should be a digit to start the reading (always read 200 lines).
	or the word "combine" to combine all files into one file.
