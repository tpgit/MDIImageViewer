:version: $RCSfile: index.rst,v $ $Revision: 693361f85272 $ $Date: 2010/08/23 15:08:52 $

=====================================================================
 mdiimageviewer -- Synchable image viewers using MDI style interface
=====================================================================

.. module:: mdiimageviewer
   :synopsis: Synchable image viewers using MDI style interface.

Inheritance Diagram
===================

.. inheritance-diagram:: mdiimageviewer


Description
===========

This module implements the :class:`MDIImageViewerWindow` class which
allows optionally synchronized panning and zooming of multiple
|QPixmap|\ s.

It contains the following classes:

+ :class:`MdiChild` -- :class:`ImageViewer <imageviewer.ImageViewer>`
  implements mouse drag panning that is activated by pressing the
  :kbd:`<Space>` key.

+ :class:`MDIImageViewerWindow` -- Views multiple images (|QPixmap|\ s)
  with optionally synchonized zooming & panning.


Reference
=========

MdiChild
--------

.. autoclass:: MdiChild
   :members:
   :show-inheritance:

MDIImageViewerWindow
--------------------

.. autoclass:: MDIImageViewerWindow
   :members:
   :show-inheritance:

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
