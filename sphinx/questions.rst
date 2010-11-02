:version: $RCSfile: index.rst,v $ $Revision: 693361f85272 $ $Date: 2010/08/23 15:08:52 $

====================================
 Remaining Implementation Questions
====================================

1. I had to specially check for :qtref:`QSettings <qsettings>` boolean
   values and convert them manually to ``bool`` (since they are
   currently stored as strings rather than something like ``@Bool``). Is
   this really necessary or the correct method when using `QVariant API
   2
   <http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/pyqt4ref.html#id12>`_?

#. For some reason, if the MDI subwindow(s) are tiled upon exit, the
   application window position & state are not correctly restored when
   the app is restarted?

#. How do you make MDI subwindows with a shorter title bar that takes up
   less vertical screen space? Setting the WindowFlags to
   ``QtCore.Qt.Tool`` results in a Tool-like window but it then is no
   longer a MDI subwindow but rather floats outside of the main window.

#. How can I specify :kbd:`NumPad /`, :kbd:`NumPad *`, and :kbd:`NumPad
   5` as keyboard shortcuts?


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
