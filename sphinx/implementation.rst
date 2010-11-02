:version: $RCSfile: index.rst,v $ $Revision: 693361f85272 $ $Date: 2010/08/23 15:08:52 $

======================
 Implementation Notes
======================

Qt Programming Notes
====================

.. currentmodule:: imageviewer

The :mod:`imageviewer` module demonstrates:

+ Using |QGraphicsView| to implement zooming & panning of a
  |QPixmap|. This works much faster for large images at high zoom levels
  than :fs:`PyQt4\\examples\\widgets\\imageviewer.pyw` which uses a
  :qtref:`QLabel <qlabel>`. The Qt documentation for the slower
  ImageViewer example is at the `nokia website
  <http://doc.qt.nokia.com/latest/widgets-imageviewer.html>`_.

+ Keeping track of scroll and view transform changes so other classes
  can implement synchronized zooming and panning of multiple views.

+ Zooming by :kbd:`Ctrl+Mouse wheel` rolling in
  :meth:`SynchableGraphicsView.wheelEvent` (|QGraphicsView| already
  handles vertical scrolling by rolling the mouse wheel, and horizontal
  scrolling via :kbd:`Alt+Mouse wheel` rolling)

.. currentmodule:: mdiimageviewer

The :mod:`mdiimageviewer` module demonstrates:

+ Synchronized zooming and panning of multiple image viewers.

+ Activating ``QtGui.QGraphicsView.ScrollHandDrag`` while the
  :kbd:`Space` key is held down in :meth:`MdiChild.keyPressEvent`.

  The documentation at
  http://doc.qt.nokia.com/latest/qwidget.html#keyReleaseEvent is a bit
  unclear. It means that ``keyReleaseEvents`` are normally not passed on
  to other classes since the default implementation is to ``accept()``
  the event.

  You have to override ``keyPressEvent`` and call ``event.ignore()`` to
  allow ``keyPressEvent``\ s to be seen by other classes.

+ Using :qtref:`QSignalMapper <qsignalmapper>` to implement a Recently
  Used Files list on the :guilabel:`File` menu in
  :meth:`MDIImageViewerWindow.updateRecentFileActions`.

+ Using :qtref:`QSignalMapper <qsignalmapper>` to call methods ---
  specified by string --- of the currently active subwindow in
  :meth:`MDIImageViewerWindow.createMappedAction`.

+ Using `shortcutContext
  <http://doc.qt.nokia.com/latest/qaction.html#shortcutContext-prop>`_
  in :meth:`MDIImageViewerWindow.createActions` to avoid
  ``QAction::eventFilter: Ambiguous shortcut overload: Ctrl+F4``
  messages::

     self._closeAct = QtGui.QAction(
         "Cl&ose", self,
         shortcut=QtGui.QKeySequence.Close,
         shortcutContext=QtCore.Qt.WidgetShortcut,
         statusTip="Close the active window",
         triggered=self._mdiArea.closeActiveSubWindow)

#. Activating the window system menu of MDI subwindows via
   :kbd:`Ctrl+Space` (:kbd:`Alt+Space` activates the Main Window system
   menu) in :meth:`MDIImageViewerWindow.createActions`. A |QAction| is
   created and ``addAction()`` of |QMainWindow| is used rather than
   adding it to a |QMenu| (since we don't want it to be a visible menu
   item).

+ Using the status bar to display image information for the currently
  active subwindow in :meth:`MDIImageViewerWindow.updateStatusBar`.
 
+ Using Qt resource files for menu icons.

+ Saving application window size & position in
  :meth:`MDIImageViewerWindow.writeSettings`.

+ Saving File Open dialog size, position & state (including selected
  filter name) in :meth:`MDIImageViewerWindow.saveDialogState`.


PyQt Programming Notes
======================

The following is done to use the more pythonic :pyqt4ref:`PyQt API
version 2 <selecting-incompatible-apis>` whether or not you are using
Python 2 or Python 3::

   import sip
   sip.setapi('QDate', 2)
   sip.setapi('QTime', 2)
   sip.setapi('QDateTime', 2)
   sip.setapi('QUrl', 2)
   sip.setapi('QTextStream', 2)
   sip.setapi('QVariant', 2)
   sip.setapi('QString', 2)

I use the :pyqt4ref:`new-style signal/slot mechanism
<new-style-signal-and-slot-support>`::

   self._mdiArea.subWindowActivated.connect(self.subWindowActivated)

rather than the :pyqt4ref:`older mechanism
<old-style-signal-and-slot-support>`::

   QtCore.QObject.connect(self._mdiArea, QtCore.SIGNAL("subWindowActivated()"), self, QtCore.SLOT("subWindowActivated()"))


I used :pyqt4ref:`pyrcc4 <pyrcc4>` to convert a Qt resource collection
file :fs:`icons.qrc` into :fs:`icons_rc.py` which can be imported into
any python file. For example the icon :fs:`exit.png` can then be
referenced simply by doing::

   import icons_rc
   ...
   self._exitAct = QtGui.QAction(
       QtGui.QIcon(':/exit.png'),
       "E&xit", self,
       shortcut=QtGui.QKeySequence.Quit,
       statusTip="Exit the application",
       triggered=QtGui.qApp.closeAllWindows)


Python Programming Notes
========================

The following is done to allow Python 3 syntax even when running Python
2.6+::

   from __future__ import division
   from __future__ import print_function
   from __future__ import unicode_literals
   from future_builtins import *

In theory these programs should work equally well under Python 3 but
that hasn't been tested yet.


Sphinx Documentation Notes
==========================

I've written all the project documentation (including these web pages)
using `Sphinx <http://sphinx.pocoo.org>`_ --- the source files can be
found on `here
<http://github.com/tpgit/MDIImageViewer/tree/master/sphinx/>`_.

The Sphinx techniques demonstrated are:

+ Generating an "orphan" Home page that uses a custom sidebar.

+ Using the `autodoc extension
  <http://sphinx.pocoo.org/ext/autodoc.html>`_ to generate the :doc:`module
  documentation <modules>`.

+ Using the `inheritance diagram extension
  <http://sphinx.pocoo.org/ext/inheritance.html>`_ to add inheritance
  diagrams to the :doc:`module documentation <modules>`.

+ Using the `extlinks extension
  <http://sphinx.pocoo.org/ext/extlinks.html>`_ to shorten references to
  the `PyQt v4 - Python Bindings for Qt v4: Reference Guide
  <http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/pyqt4ref.html>`_
  and the `Qt Class Documentation
  <http://doc.qt.nokia.com/latest/classes.html>`_.

+ Creating a custom theme (based of the `default
  <http://sphinx.pocoo.org/theming.html#builtin-themes>`_ theme) to have
  a custom footer with the `Creative Commons Attribution 3.0
  <http://creativecommons.org/licenses/by/3.0/us/>`_ Licence & logo
  rather than a copyright notice. I also have a custom ``css`` file to
  style some elements differently than the defaults.

+ Using a global Table of Contents in the sidebar navigation panel with
  the current page indicated with a yellowish bullet. Most of the sites
  I've seen use the local TOC which means you have to jump back to their
  separate Table of Contents page to get a site overview.

+ Using the ``rst_prolog`` :fs:`conf.py` setting to create a custom
  ``role`` that can be used in any of the source directory's :fs:`.rst`
  files.

+ Using the ``rst_prolog`` :fs:`conf.py` setting to create quick
  replacements for common Qt Class documentation links. For example,
  ``|QGraphicsView|`` generates the following link:
  |QGraphicsView|. These replacements even work inside Python
  docstrings.

Project Hosting on GitHub Notes
===============================

You can directly use Sphinx generated pages as `GitHub Pages
<http://pages.github.com/>`_, but as the "Using Jekyll For Complex
Layouts" section explains:

   "As of December 27, 2009, you can completely opt-out of Jekyll
   processing by creating a file named :fs:`.nojekyll` in the root of
   your pages repo and pushing that to GitHub. This should only be
   necessary if your site uses directories that begin with an
   underscore, as Jekyll sees these as special dirs and does not copy
   them to the final destination."

Since Sphinx generates a number of subdirectories that start with ``_``
in its build directory, adding :fs:`.nojekyll` is thus required.

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
