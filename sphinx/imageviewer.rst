:version: $RCSfile: index.rst,v $ $Revision: 693361f85272 $ $Date: 2010/08/23 15:08:52 $

======================================================
 imageviewer -- Image viewer with panning and zooming
======================================================

.. module:: imageviewer
   :synopsis: Image viewer with panning and zooming.

Inheritance Diagram
===================

.. inheritance-diagram:: imageviewer


Description
===========

This module implements the :class:`ImageViewer` class which allows
panning and zooming of |QPixmap|\ s by using a
:class:`SynchableGraphicsView` embedded inside a :qtref:`QFrame
<qframe>`.

It contains the following classes:

+ :class:`ImageViewer` -- Image Viewer than can pan & zoom images
  (|QPixmap|\ s).

+ :class:`SynchableGraphicsView` -- |QGraphicsView| that can synchronize
  zooming & panning of multiple instances.

+ :class:`MainWindow` -- Sample app to test the :class:`ImageViewer` class.

Reference
=========

ImageViewer
-----------

.. autoclass:: ImageViewer
   :members:
   :show-inheritance:

SynchableGraphicsView
---------------------

.. autoclass:: SynchableGraphicsView
   :members:
   :show-inheritance:

MainWindow
----------

.. autoclass:: MainWindow
   :members:
   :show-inheritance:

   **Usage**::

     python imageviewer.py imagefilename

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
