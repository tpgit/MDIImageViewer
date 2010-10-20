.. -*- mode: rst -*-

================================
 MDI Image Viewer sample README
================================

Introduction
============

I'm trying to write my first PyQt program. I eventually plan on creating
an open-source PyQt app that explores the use of various image processing
operations (using the Leptonica C library http://www.leptonica.com as
the underlying image processing engine).

One of my initial goals is to be able to view multiple QPixmaps while
optionally keeping their view's pan and zoom values synchronized (so you
can easily compare the results of the image processing operations).

I've managed to write an MDI Image Viewer and I put what I've come up
with so far at: http://github.com/tpgit/MDIImageViewer

I'd like to make sure I am following PyQt & Python "good practices"
before going on to create my "real" application. I'd appreciate any
comments on the overall architecture & implementation. It could very
well be that I should really be using dip
(http://www.riverbankcomputing.co.uk/software/dip/intro) even though
it's pretty new? (As far as Python style goes let me warn you that I use
camelcase naming and prefix "private" data member names with a _.)

I've used Sphinx (http://sphinx.pocoo.org/) to do general documentation,
but haven't yet tried it for documenting python sources. I assume that
I'll have to add to my existing docstrings to document parameters and
return values?

As far as testing goes, I not sure how one goes about testing PyQt GUI
apps other than using them?


File Descriptions
=================

Here's a brief description of the two main python files following by
some remaining implementation questions.

imageviewer.py demonstrates:

+ Using QGraphicsView to implement zooming & panning of a pixmap. This
  works much faster for large images at high zoom levels than
  PyQt4\examples\widgets\imageviewer.pyw which uses a QLabel.

+ Keeping track of scroll & view changes so other classes can implement
  synchronized zooming and panning of multiple views.

+ Zooming by Ctrl+Mouse wheel rolling. (QGraphicsView already handles vertical
  scrolling by rolling mouse wheel, and horizontal scrolling via
  Alt+Mouse wheel rolling)

mdiimageviewer.py demonstrates:

+ Synchronized zooming and panning of multiple image viewers.

+ Activating QtGui.QGraphicsView.ScrollHandDrag while the <Space> key is
  held down.

  The documentation at
  http://doc.qt.nokia.com/4.7/qwidget.html#keyReleaseEvent is a bit
  unclear. It means that keyReleaseEvents are normally not passed on to
  other classes since the default implementation is to accept() the
  event.

  You have to override keyPressEvent and call event.ignore() to allow
  keyPressEvents to be seen by other classes.

+ Using QSignalMapper to implement a Recently Used Files list on the
  File menu.

+ Using QSignalMapper to call methods specified by string of the
  currently active subwindow.

+ Using the status bar to display image information for the currently
  active subwindow.
 
+ Using Qt resource files for menu icons.

+ Saving application window size & position.

+ Saving File Open dialog size, position & state (including selected
  filter name).


Remaining Questions
===================

I had to specially check for QSettings boolean values and convert them
manually to bool (since they are currently stored as strings rather than
something like @Bool). Is this really necessary or the correct method
when using QVariant API 2?

For some reason, if the MDI subwindow(s) are tiled upon exit, the
application window position & state are not correctly restored when the
app is restarted?

How do you make MDI subwindows with a shorter title bar that takes up
less vertical screen space? Setting the WindowFlags to QtCore.Qt.Tool
results in a Tool-like window but it then is no longer a MDI subwindow
but rather floats outside of the main window.

How can I specify NumPad /, NumPad *, and NumPad 5 as keyboard
shortcuts?

The Ctrl+F4 shortcut key doesn't work to close MDI subwindows? If you
specify QtGui.QKeySequence.Close it shows up on the menu item and the
menu item works but typing the shortcut does nothing. The standard
Ctrl+W also doesn't work. (F4 works but I ended up using the non-standard
Ctrl+Alt+F4 instead.)

How do you activate the window system menu of the MDI subwindows? On
Microsoft Windows XP this is normally done with Ctrl+Space (Alt+Space
activates the Main Window system menu).

 (Ctrl+Space didn't activate the MDI subwindow System Menu until I
 specifically added an action with that shortcut to my menu. It should
 really happen automatically without having to have a visible menu item
 in the main window menubar.)

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
