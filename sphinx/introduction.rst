:version: $RCSfile: index.rst,v $ $Revision: 693361f85272 $ $Date: 2010/08/23 15:08:52 $

==============
 Introduction
==============

Motivation
==========

I am in the process of creating an open-source PyQt app that explores
the use of various image processing operations (using the Leptonica C
library http://www.leptonica.com as the underlying image processing
engine). One of my initial goals was to be able to view multiple
|QPixmap|\ s while optionally keeping their view's pan and zoom values
synchronized (so you can easily compare the results of the image
processing operations).

As a first step I've managed to come up with the application described
in these pages, but I'd like to make sure I am following PyQt & Python
"good practices" before going on to create my "real" application. I'd
appreciate any comments on the overall architecture & implementation. It
could very well be that I should be using `dip
<http://www.riverbankcomputing.co.uk/software/dip/intro>`_ even though
it's pretty new? (As far as Python style goes let me warn you that I use
camelCase naming and prefix "private" data member names with a ``_``.)

You can send a message to ``tpgit`` via GitHub, leave comments on the
Project's `issues <http://github.com/tpgit/MDIImageViewer/issues>`_
page, or post them to the `PyQt Mailing List
<mailto:pyqt@riverbankcomputing.com>`_ or `Qt Mailing List
<http://lists.trolltech.com/mailman/listinfo/qt-interest>`_ with a
subject containing "PyQt MDI Image Viewer".

.. todo::

   Incorporate suggestions from feedback.

Prequisites
===========

`Python 2.6 <http://python.org/download/releases/>`_ is required (it
will probably run under Python 2.7 and Python 3). For Windows I highly
recommend `ActiveState Python
<http://www.activestate.com/activepython/downloads>`_.

You'll also need `PyQt 4.x
<http://www.riverbankcomputing.co.uk/software/pyqt/download>`_ for the
corresponding version of Python.

If you want to regenerate the documentation from the :fs:`.rst` sources
you'll need `Sphinx <http://sphinx.pocoo.org/index.html>`_.


Installation
============

You can either download a tarball or zipfile from `here
<http://github.com/tpgit/MDIImageViewer/archives/master>`_ or clone the
`repository <http://github.com/tpgit/MDIImageViewer>`_ using `git
<http://git-scm.com/>`_.

Usage
=====

To use the MDI Image Viewer open up a Command Prompt, switch to the main
MDI Image Viewer directory, and enter::

   python mdiimageviewer.py

If you want to test the single Image Viewer::

   python imageviewer.py imagefilename

this will print out debugging messages to ``stdout`` as various
``signals`` are generated.

..
   Local Variables:
   coding: utf-8
   mode: rst
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 72
   mode: auto-fill
   standard-indent: 3
   tab-stop-list: (3 6 9 12 15 18 21 24 27 30 33 36 39 42 45 48 51 54 57 60)
   End:
