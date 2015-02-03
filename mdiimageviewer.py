#!/usr/bin/env python
# $RCSfile: mdiimageviewer.pyw,v $ $Revision: 00c5d1c96a3b $ $Date: 2010/10/18 20:43:38 $

"""
MDI Image Viewer Window

based on PyQt MDI.py example.

"""

# ====================================================================

#from __future__ import division
#from __future__ import print_function
#from __future__ import unicode_literals
#from future_builtins import *

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QDate', 2)
sip.setapi('QTime', 2)
sip.setapi('QDateTime', 2)
sip.setapi('QUrl', 2)
sip.setapi('QTextStream', 2)
sip.setapi('QVariant', 2)
sip.setapi('QString', 2)

# ====================================================================

from PyQt5 import QtCore, QtGui,  QtWidgets

import imageviewer
import icons_rc

__version__ = "1.0.0"
COMPANY = "TPWorks"
DOMAIN = "dummy-tpworks.com"
APPNAME = "MDI Image Viewer"

SETTING_RECENTFILELIST = "recentfilelist"
SETTING_FILEOPEN = "fileOpenDialog"
SETTING_SCROLLBARS = "scrollbars"
SETTING_STATUSBAR = "statusbar"
SETTING_SYNCHZOOM = "synchzoom"
SETTING_SYNCHPAN = "synchpan"

# ====================================================================

def toBool(value):
    """
    Module function to convert a value to bool.

    :param value: value to be converted
    :returns:     converted data
    """
    if value in ["true", "1", "True"]:
        return True
    elif value in ["false", "0", "False"]:
        return False
    else:
        return bool(value)

def strippedName(fullFilename):
    return QtCore.QFileInfo(fullFilename).fileName()

# ====================================================================

class MdiChild(imageviewer.ImageViewer):
    """ImageViewer that implements <Space> key pressed panning."""

    def __init__(self, pixmap, filename, name):
        """:param pixmap: |QPixmap| to display
        :type pixmap: |QPixmap| or None
        :param filename: |QPixmap| filename
        :type filename: str or None
        :param name: name associated with this ImageViewer
        :type name: str or None"""
        super(MdiChild, self).__init__(pixmap, name)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self._isUntitled = True
        self.currentFile = filename

    # ------------------------------------------------------------------

    @property
    def currentFile(self):
        """Current filename (*str*)."""
        return self._currentFile

    @currentFile.setter
    def currentFile(self, filename):
        self._currentFile = QtCore.QFileInfo(filename).canonicalFilePath()
        self._isUntitled = False
        self.setWindowTitle(self.userFriendlyCurrentFile)

    @property
    def userFriendlyCurrentFile(self):
        """Get current filename without path (*str*)."""
        if self.currentFile:
            return strippedName(self.currentFile)
        else:
            return ""

    # ------------------------------------------------------------------

    def keyPressEvent(self, keyEvent):
        """Overrides to enable panning while dragging.

        :param QKeyEvent keyEvent: instance of |QKeyEvent|"""

        assert isinstance(keyEvent, QtGui.QKeyEvent)
        if keyEvent.key() == QtCore.Qt.Key_Space:
            if (not keyEvent.isAutoRepeat() and
                not self.handDragging):
                self.enableHandDrag(True)
            keyEvent.accept()
        else:
            keyEvent.ignore()
        super(MdiChild, self).keyPressEvent(keyEvent)

    def keyReleaseEvent(self, keyEvent):
        """Overrides to disable panning while dragging.

        :param QKeyEvent keyEvent: instance of |QKeyEvent|"""
        assert isinstance(keyEvent, QtGui.QKeyEvent)
        if keyEvent.key() == QtCore.Qt.Key_Space:
            if (not keyEvent.isAutoRepeat() and
                self.handDragging):
                self.enableHandDrag(False)
            keyEvent.accept()
        else:
            keyEvent.ignore()
        super(MdiChild, self).keyReleaseEvent(keyEvent)

# ====================================================================

class MDIImageViewerWindow(QtWidgets.QMainWindow):
    """Views multiple images with optionally synchonized zooming & panning."""

    MaxRecentFiles = 10

    def __init__(self):
        super(MDIImageViewerWindow, self).__init__()

        self._recentFileActions = []
        self._handlingScrollChangedSignal = False

        self._mdiArea = QtWidgets.QMdiArea()
        self._mdiArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self._mdiArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self._mdiArea.subWindowActivated.connect(self.subWindowActivated)
        self.setCentralWidget(self._mdiArea)
        #self._mdiArea.setViewMode(QtWidgets.QMdiArea.TabbedView)

        self._mdiArea.subWindowActivated.connect(self.updateMenus)

        self._windowMapper = QtCore.QSignalMapper(self)
        self._windowMapper.mapped[QtWidgets.QWidget].connect(self.setActiveSubWindow)

        self._actionMapper = QtCore.QSignalMapper(self)
        self._actionMapper.mapped[str].connect(self.mappedImageViewerAction)
        self._recentFileMapper = QtCore.QSignalMapper(self)
        self._recentFileMapper.mapped[str].connect(self.openRecentFile)

        self.createActions()
        self.addAction(self._activateSubWindowSystemMenuAct)

        self.createMenus()
        self.updateMenus()
        self.createStatusBar()

        self.readSettings()
        self.updateStatusBar()


        self.setUnifiedTitleAndToolBarOnMac(True)

    # ------------------------------------------------------------------

    def createMappedAction(self, icon, text, parent, shortcut, methodName):
        """Create |QAction| that is mapped via methodName to call.

        :param icon: icon associated with |QAction|
        :type icon: |QIcon| or None
        :param str text: the |QAction| descriptive text
        :param QObject parent: the parent |QObject|
        :param QKeySequence shortcut: the shortcut |QKeySequence|
        :param str methodName: name of method to call when |QAction| is
                               triggered
        :rtype: |QAction|"""

        if icon is not None:
            action = QtWidgets.QAction(icon, text, parent,
                                   shortcut=shortcut,
                                   triggered=self._actionMapper.map)
        else:
            action = QtWidgets.QAction(text, parent,
                                   shortcut=shortcut,
                                   triggered=self._actionMapper.map)
        self._actionMapper.setMapping(action, methodName)
        return action

    def createActions(self):
        """Create actions used in menus."""
        #File menu actions
        self._openAct = QtWidgets.QAction(
            QtGui.QIcon(':/open.png'),
            "&Open...", self,
            shortcut=QtGui.QKeySequence.Open,
            statusTip="Open an existing file",
            triggered=self.open)

        self._switchLayoutDirectionAct = QtWidgets.QAction(
            "Switch &layout direction", self,
            triggered=self.switchLayoutDirection)

        #create dummy recent file actions
        for i in range(MDIImageViewerWindow.MaxRecentFiles):
            self._recentFileActions.append(
                QtWidgets.QAction(self, visible=False,
                              triggered=self._recentFileMapper.map))

        self._exitAct = QtWidgets.QAction(
            QtGui.QIcon(':/exit.png'),
            "E&xit", self,
            shortcut=QtGui.QKeySequence.Quit,
            statusTip="Exit the application",
            triggered=QtWidgets.qApp.closeAllWindows)

        #View menu actions
        self._showScrollbarsAct = QtWidgets.QAction(
            "&Scrollbars", self,
            checkable=True,
            statusTip="Toggle display of subwindow scrollbars",
            triggered=self.toggleScrollbars)

        self._showStatusbarAct = QtWidgets.QAction(
            "S&tatusbar", self,
            checkable=True,
            statusTip="Toggle display of statusbar",
            triggered=self.toggleStatusbar)

        self._synchZoomAct = QtWidgets.QAction(
            "Synch &Zoom", self,
            checkable=True,
            statusTip="Synch zooming of subwindows",
            triggered=self.toggleSynchZoom)

        self._synchPanAct = QtWidgets.QAction(
            "Synch &Pan", self,
            checkable=True,
            statusTip="Synch panning of subwindows",
            triggered=self.toggleSynchPan)

        #Scroll menu actions
        self._scrollActions = [
            self.createMappedAction(
                None,
                "&Top", self,
                QtGui.QKeySequence.MoveToStartOfDocument,
                "scrollToTop"),

            self.createMappedAction(
                None,
                "&Bottom", self,
                QtGui.QKeySequence.MoveToEndOfDocument,
                "scrollToBottom"),

            self.createMappedAction(
                None,
                "&Left Edge", self,
                QtGui.QKeySequence.MoveToStartOfLine,
                "scrollToBegin"),

            self.createMappedAction(
                None,
                "&Right Edge", self,
                QtGui.QKeySequence.MoveToEndOfLine,
                "scrollToEnd"),

            self.createMappedAction(
                None,
                "&Center", self,
                "5",
                "centerView"),
            ]

        #zoom menu actions
        separatorAct = QtWidgets.QAction(self)
        separatorAct.setSeparator(True)

        self._zoomActions = [
            self.createMappedAction(
                QtGui.QIcon(':/zoomin.png'),
                "Zoo&m In (25%)", self,
                QtGui.QKeySequence.ZoomIn,
                "zoomIn"),

            self.createMappedAction(
                QtGui.QIcon(':/zoomout.png'),
                "Zoom &Out (25%)", self,
                QtGui.QKeySequence.ZoomOut,
                "zoomOut"),

            #self.createMappedAction(
                #None,
                #"&Zoom To...", self,
                #"Z",
                #"zoomTo"),

            separatorAct,

            self.createMappedAction(
                None,
                "Actual &Size", self,
                "/",
                "actualSize"),

            self.createMappedAction(
                None,
                "Fit &Image", self,
                "*",
                "fitToWindow"),

            self.createMappedAction(
                None,
                "Fit &Width", self,
                "Alt+Right",
                "fitWidth"),

            self.createMappedAction(
                None,
                "Fit &Height", self,
                "Alt+Down",
                "fitHeight"),
           ]

        #Window menu actions
        self._activateSubWindowSystemMenuAct = QtWidgets.QAction(
            "Activate &System Menu", self,
            shortcut="Ctrl+ ",
            statusTip="Activate subwindow System Menu",
            triggered=self.activateSubwindowSystemMenu)

        self._closeAct = QtWidgets.QAction(
            "Cl&ose", self,
            shortcut=QtGui.QKeySequence.Close,
            shortcutContext=QtCore.Qt.WidgetShortcut,
            #shortcut="Ctrl+Alt+F4",
            statusTip="Close the active window",
            triggered=self._mdiArea.closeActiveSubWindow)

        self._closeAllAct = QtWidgets.QAction(
            "Close &All", self,
            statusTip="Close all the windows",
            triggered=self._mdiArea.closeAllSubWindows)

        self._tileAct = QtWidgets.QAction(
            "&Tile", self,
            statusTip="Tile the windows",
            triggered=self._mdiArea.tileSubWindows)

        self._cascadeAct = QtWidgets.QAction(
            "&Cascade", self,
            statusTip="Cascade the windows",
            triggered=self._mdiArea.cascadeSubWindows)

        self._nextAct = QtWidgets.QAction(
            "Ne&xt", self,
            shortcut=QtGui.QKeySequence.NextChild,
            statusTip="Move the focus to the next window",
            triggered=self._mdiArea.activateNextSubWindow)

        self._previousAct = QtWidgets.QAction(
            "Pre&vious", self,
            shortcut=QtGui.QKeySequence.PreviousChild,
            statusTip="Move the focus to the previous window",
            triggered=self._mdiArea.activatePreviousSubWindow)

        self._separatorAct = QtWidgets.QAction(self)
        self._separatorAct.setSeparator(True)

        self._aboutAct = QtWidgets.QAction(
            QtGui.QIcon(':/help.png'),
            "&About", self,
            statusTip="Show the application's About box",
            triggered=self.about)

        self._aboutQtAct = QtWidgets.QAction(
            QtGui.QIcon(':/qt.png'),
            "About &Qt", self,
            statusTip="Show the Qt library's About box",
            triggered=QtWidgets.qApp.aboutQt)

    def createMenus(self):
        """Create menus."""
        self._fileMenu = self.menuBar().addMenu("&File")
        self._fileMenu.addAction(self._openAct)
        self._fileMenu.addAction(self._switchLayoutDirectionAct)

        self._fileSeparatorAct = self._fileMenu.addSeparator()
        for action in self._recentFileActions:
            self._fileMenu.addAction(action)
        self.updateRecentFileActions()
        self._fileMenu.addSeparator()
        self._fileMenu.addAction(self._exitAct)

        self._viewMenu = self.menuBar().addMenu("&View")
        self._viewMenu.addAction(self._showScrollbarsAct)
        self._viewMenu.addAction(self._showStatusbarAct)
        self._viewMenu.addSeparator()
        self._viewMenu.addAction(self._synchZoomAct)
        self._viewMenu.addAction(self._synchPanAct)

        self._scrollMenu = self.menuBar().addMenu("&Scroll")
        [self._scrollMenu.addAction(action) for action in self._scrollActions]

        self._zoomMenu = self.menuBar().addMenu("&Zoom")
        [self._zoomMenu.addAction(action) for action in self._zoomActions]

        self._windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self._windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self._helpMenu = self.menuBar().addMenu("&Help")
        self._helpMenu.addAction(self._aboutAct)
        self._helpMenu.addAction(self._aboutQtAct)

    def updateMenus(self):
        """Update menus."""
        hasMdiChild = (self.activeMdiChild is not None)

        self._scrollMenu.setEnabled(hasMdiChild)
        self._zoomMenu.setEnabled(hasMdiChild)

        self._closeAct.setEnabled(hasMdiChild)
        self._closeAllAct.setEnabled(hasMdiChild)

        self._tileAct.setEnabled(hasMdiChild)
        self._cascadeAct.setEnabled(hasMdiChild)
        self._nextAct.setEnabled(hasMdiChild)
        self._previousAct.setEnabled(hasMdiChild)
        self._separatorAct.setVisible(hasMdiChild)

    def updateRecentFileActions(self):
        """Update recent file menu items."""
        settings = QtCore.QSettings()
        files = settings.value(SETTING_RECENTFILELIST)
        numRecentFiles = min(len(files) if files else 0,
                             MDIImageViewerWindow.MaxRecentFiles)

        for i in range(numRecentFiles):
            text = "&%d %s" % (i + 1, strippedName(files[i]))
            self._recentFileActions[i].setText(text)
            self._recentFileActions[i].setData(files[i])
            self._recentFileActions[i].setVisible(True)
            self._recentFileMapper.setMapping(self._recentFileActions[i],
                                              files[i])

        for j in range(numRecentFiles, MDIImageViewerWindow.MaxRecentFiles):
            self._recentFileActions[j].setVisible(False)

        self._fileSeparatorAct.setVisible((numRecentFiles > 0))

    def updateWindowMenu(self):
        """Update the Window menu."""
        self._windowMenu.clear()
        self._windowMenu.addAction(self._closeAct)
        self._windowMenu.addAction(self._closeAllAct)
        self._windowMenu.addSeparator()
        self._windowMenu.addAction(self._tileAct)
        self._windowMenu.addAction(self._cascadeAct)
        self._windowMenu.addSeparator()
        self._windowMenu.addAction(self._nextAct)
        self._windowMenu.addAction(self._previousAct)
        self._windowMenu.addAction(self._separatorAct)

        windows = self._mdiArea.subWindowList()
        self._separatorAct.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.userFriendlyCurrentFile)
            if i < 9:
                text = '&' + text

            action = self._windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child == self.activeMdiChild)
            action.triggered.connect(self._windowMapper.map)
            self._windowMapper.setMapping(action, window)

    def createStatusBarLabel(self, stretch=0):
        """Create status bar label.

        :param int stretch: stretch factor
        :rtype: |QLabel|"""
        label = QtWidgets.QLabel()
        label.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        label.setLineWidth(2)
        self.statusBar().addWidget(label, stretch)
        return label

    def createStatusBar(self):
        """Create status bar."""
        statusBar = self.statusBar()

        self._sbLabelName = self.createStatusBarLabel(1)
        self._sbLabelSize = self.createStatusBarLabel()
        self._sbLabelDimensions = self.createStatusBarLabel()
        self._sbLabelDate = self.createStatusBarLabel()
        self._sbLabelZoom = self.createStatusBarLabel()

        statusBar.showMessage("Ready")

    # ------------------------------------------------------------------

    @property
    def activeMdiChild(self):
        """Get active MDI child (:class:`MdiChild` or *None*)."""
        activeSubWindow = self._mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    # ------------------------------------------------------------------

    #overriden methods

    def closeEvent(self, event):
        """Overrides close event to save application settings.

        :param QEvent event: instance of |QEvent|"""
        self._mdiArea.closeAllSubWindows()
        if self.activeMdiChild:
            event.ignore()
        else:
            self.writeSettings()
            event.accept()

    # ------------------------------------------------------------------

    @QtCore.pyqtSlot(str)
    def mappedImageViewerAction(self, methodName):
        """Perform action mapped to :class:`imageviewer.ImageViewer`
        methodName.

        :param str methodName: method to call"""
        activeViewer = self.activeMdiChild
        if hasattr(activeViewer, str(methodName)):
            getattr(activeViewer, str(methodName))()

    @QtCore.pyqtSlot()
    def toggleSynchPan(self):
        """Toggle synchronized subwindow panning."""
        if self._synchPanAct.isChecked():
            self.synchPan(self.activeMdiChild)

    @QtCore.pyqtSlot()
    def panChanged(self):
        """Synchronize subwindow pans."""
        mdiChild = self.sender()
        while mdiChild is not None and type(mdiChild) != MdiChild:
            mdiChild = mdiChild.parent()
        if mdiChild and self._synchPanAct.isChecked():
            self.synchPan(mdiChild)

    @QtCore.pyqtSlot()
    def toggleSynchZoom(self):
        """Toggle synchronized subwindow zooming."""
        if self._synchZoomAct.isChecked():
            self.synchZoom(self.activeMdiChild)

    @QtCore.pyqtSlot()
    def zoomChanged(self):
        """Synchronize subwindow zooms."""
        mdiChild = self.sender()
        if self._synchZoomAct.isChecked():
            self.synchZoom(mdiChild)
        self.updateStatusBar()

    @QtCore.pyqtSlot()
    def activateSubwindowSystemMenu(self):
        """Activate current subwindow's System Menu."""
        activeSubWindow = self._mdiArea.activeSubWindow()
        if activeSubWindow:
            activeSubWindow.showSystemMenu()

    @QtCore.pyqtSlot(str)
    def openRecentFile(self, filename):
        """Open a recent file.

        :param str filename: filename to view"""
        self.loadFile(filename)

    @QtCore.pyqtSlot()
    def open(self):
        """Handle the open action."""
        fileDialog = QtWidgets.QFileDialog(self)
        settings = QtCore.QSettings()
        fileDialog.setNameFilters(["Image Files (*.jpg *.png *.tif)",
                                   "All Files (*)"])
        if not settings.contains(SETTING_FILEOPEN + "/state"):
            fileDialog.setDirectory(".")
        else:
            self.restoreDialogState(fileDialog, SETTING_FILEOPEN)
        fileDialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if not fileDialog.exec_():
            return
        self.saveDialogState(fileDialog, SETTING_FILEOPEN)

        filename = fileDialog.selectedFiles()[0]
        self.loadFile(filename)

    @QtCore.pyqtSlot()
    def toggleScrollbars(self):
        """Toggle subwindow scrollbar visibility."""
        checked = self._showScrollbarsAct.isChecked()

        windows = self._mdiArea.subWindowList()
        for window in windows:
            child = window.widget()
            child.enableScrollBars(checked)

    @QtCore.pyqtSlot()
    def toggleStatusbar(self):
        """Toggle status bar visibility."""
        self.statusBar().setVisible(self._showStatusbarAct.isChecked())

    @QtCore.pyqtSlot()
    def about(self):
        """Display About dialog box."""
        QtWidgets.QMessageBox.about(self, "About MDI",
                "<b>MDI Image Viewer</b> demonstrates how to"
                "synchronize the panning and zooming of multiple image"
                "viewer windows using Qt.")

    @QtCore.pyqtSlot(QtWidgets.QMdiSubWindow)
    def subWindowActivated(self, window):
        """Handle |QMdiSubWindow| activated signal.

        :param |QMdiSubWindow| window: |QMdiSubWindow| that was just
                                       activated"""
        self.updateStatusBar()

    @QtCore.pyqtSlot(QtWidgets.QMdiSubWindow)
    def setActiveSubWindow(self, window):
        """Set active |QMdiSubWindow|.

        :param |QMdiSubWindow| window: |QMdiSubWindow| to activate """
        if window:
            self._mdiArea.setActiveSubWindow(window)

    # ------------------------------------------------------------------

    def loadFile(self, filename):
        """Load filename into new :class:`MdiChild` window.

        :param str filename: filename to load"""
        activeMdiChild = self.activeMdiChild
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        pixmap = QtGui.QPixmap(filename)
        QtWidgets.QApplication.restoreOverrideCursor()
        if (not pixmap or
            pixmap.width()==0 or pixmap.height==0):
            QtWidgets.QMessageBox.warning(self, APPNAME,
                                      "Cannot read file %s." % (filename,))
            self.updateRecentFileSettings(filename, delete=True)
            self.updateRecentFileActions()
            return

        child = self.createMdiChild(pixmap, filename)
        child.show()

        if activeMdiChild:
            if self._synchPanAct.isChecked():
                self.synchPan(activeMdiChild)
            if self._synchZoomAct.isChecked():
                self.synchZoom(activeMdiChild)

        self.updateRecentFileSettings(filename)
        self.updateRecentFileActions()

        self.statusBar().showMessage("File loaded", 2000)

    def updateStatusBar(self):
        """Update status bar."""
        self.statusBar().setVisible(self._showStatusbarAct.isChecked())
        imageViewer = self.activeMdiChild
        if not imageViewer:
            self._sbLabelName.setText("")
            self._sbLabelSize.setText("")
            self._sbLabelDimensions.setText("")
            self._sbLabelDate.setText("")
            self._sbLabelZoom.setText("")

            self._sbLabelSize.hide()
            self._sbLabelDimensions.hide()
            self._sbLabelDate.hide()
            self._sbLabelZoom.hide()
            return

        filename = imageViewer.currentFile
        self._sbLabelName.setText(" %s " % filename)

        fi = QtCore.QFileInfo(filename)
        size = fi.size()
        fmt = " %.1f %s "
        if size > 1024*1024*1024:
            unit = "MB"
            size /= 1024*1024*1024
        elif size > 1024*1024:
            unit = "MB"
            size /= 1024*1024
        elif size > 1024:
            unit = "KB"
            size /= 1024
        else:
            unit = "Bytes"
            fmt = " %d %s "
        self._sbLabelSize.setText(fmt % (size, unit))

        pixmap = imageViewer.pixmap
        self._sbLabelDimensions.setText(" %dx%dx%d " %
                                        (pixmap.width(),
                                         pixmap.height(),
                                         pixmap.depth()))

        self._sbLabelDate.setText(
            " %s " %
            fi.lastModified().toString(QtCore.Qt.SystemLocaleShortDate))
        self._sbLabelZoom.setText(" %0.f%% " % (imageViewer.zoomFactor*100,))

        self._sbLabelSize.show()
        self._sbLabelDimensions.show()
        self._sbLabelDate.show()
        self._sbLabelZoom.show()

    def createMdiChild(self, pixmap, filename):
        """Create new :class:`MdiChild` for pixmap.

        :param pixmap: |QPixmap| to display in :class:`MdiChild`
        :type pixmap: |QPixmap| or None
        :param filename: |QPixmap| filename
        :type filename: str or None
        :rtype: :class:`MdiChild`"""

        child = MdiChild(pixmap,
                         filename,
                         "Child %d" % (len(self._mdiArea.subWindowList())+1))
        child.enableScrollBars(self._showScrollbarsAct.isChecked())
        window = self._mdiArea.addSubWindow(child)

        child.scrollChanged.connect(self.panChanged)
        child.transformChanged.connect(self.zoomChanged)

        return child

    def switchLayoutDirection(self):
        """Switch MDI subwindow layout direction."""
        if self.layoutDirection() == QtCore.Qt.LeftToRight:
            QtWidgets.qApp.setLayoutDirection(QtCore.Qt.RightToLeft)
        else:
            QtWidgets.qApp.setLayoutDirection(QtCore.Qt.LeftToRight)

    def synchPan(self, fromViewer):
        """Synch panning of all subwindowws to the same as *fromViewer*.

        :param fromViewer: :class:`MdiChild` that initiated synching"""
        assert isinstance(fromViewer, MdiChild)
        if not fromViewer:
            return
        if self._handlingScrollChangedSignal:
            return
        self._handlingScrollChangedSignal = True

        newState = fromViewer.scrollState
        changedWindow = fromViewer.parent()
        windows = self._mdiArea.subWindowList()
        for window in windows:
            if window != changedWindow:
                window.widget().scrollState = newState
        self._handlingScrollChangedSignal = False

    def synchZoom(self, fromViewer):
        """Synch zoom of all subwindowws to the same as *fromViewer*.

        :param fromViewer: :class:`MdiChild` that initiated synching"""
        if not fromViewer:
            return
        newZoomFactor = fromViewer.zoomFactor
        changedWindow = fromViewer.parent()
        windows = self._mdiArea.subWindowList()
        for window in windows:
            if window != changedWindow:
                window.widget().zoomFactor = newZoomFactor

    # ------------------------------------------------------------------

    def saveDialogState(self, dialog, groupName):
        """Save dialog state, position & size.

        :param |QDialog| dialog: dialog to save state of
        :param str groupName: |QSettings| group name"""
        assert isinstance(dialog, QtWidgets.QDialog)

        settings = QtCore.QSettings()
        settings.beginGroup(groupName)

        settings.setValue('state', dialog.saveState())
        settings.setValue('geometry', dialog.saveGeometry())
        settings.setValue('filter', dialog.selectedNameFilter())

        settings.endGroup()

    def restoreDialogState(self, dialog, groupName):
        """Restore dialog state, position & size.

        :param str groupName: |QSettings| group name"""
        assert isinstance(dialog, QtWidgets.QDialog)

        settings = QtCore.QSettings()
        settings.beginGroup(groupName)

        dialog.restoreState(settings.value('state'))
        dialog.restoreGeometry(settings.value('geometry'))
        dialog.selectNameFilter(settings.value('filter', ""))

        settings.endGroup()

    def writeSettings(self):
        """Write application settings."""
        settings = QtCore.QSettings()
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())
        settings.setValue('windowgeometry', self.saveGeometry())
        settings.setValue('windowstate', self.saveState())

        settings.setValue(SETTING_SCROLLBARS,
                          self._showScrollbarsAct.isChecked())
        settings.setValue(SETTING_STATUSBAR,
                          self._showStatusbarAct.isChecked())
        settings.setValue(SETTING_SYNCHZOOM,
                          self._synchZoomAct.isChecked())
        settings.setValue(SETTING_SYNCHPAN,
                          self._synchPanAct.isChecked())

    def readSettings(self):
        """Read application settings."""
        settings = QtCore.QSettings()
        pos = settings.value('pos', QtCore.QPoint(200, 200))
        size = settings.value('size', QtCore.QSize(400, 400))
        self.move(pos)
        self.resize(size)
        if settings.contains('windowgeometry'):
            self.restoreGeometry(settings.value('windowgeometry'))
        if settings.contains('windowstate'):
            self.restoreState(settings.value('windowstate'))

        self._showScrollbarsAct.setChecked(
            toBool(settings.value(SETTING_SCROLLBARS, True)))
        self._showStatusbarAct.setChecked(
            toBool(settings.value(SETTING_STATUSBAR, True)))
        self._synchZoomAct.setChecked(
            toBool(settings.value(SETTING_SYNCHZOOM, True)))
        self._synchPanAct.setChecked(
            toBool(settings.value(SETTING_SYNCHPAN, True)))

    def updateRecentFileSettings(self, filename, delete=False):
        """Update recent file list setting.

        :param str filename: filename to add or remove from recent file
                             list
        :param bool delete: if True then filename removed, otherwise added"""
        settings = QtCore.QSettings()
        files = list(settings.value(SETTING_RECENTFILELIST, []))

        try:
            files.remove(filename)
        except ValueError:
            pass

        if not delete:
            files.insert(0, filename)
        del files[MDIImageViewerWindow.MaxRecentFiles:]

        settings.setValue(SETTING_RECENTFILELIST, files)


# ====================================================================

def main():
    """Run MDI Image Viewer application."""
    import sys

    app = QtWidgets.QApplication(sys.argv)
    QtCore.QSettings.setDefaultFormat(QtCore.QSettings.IniFormat)
    app.setOrganizationName(COMPANY)
    app.setOrganizationDomain(DOMAIN)
    app.setApplicationName(APPNAME)
    app.setWindowIcon(QtGui.QIcon(":/icon.png"))

    mainWin = MDIImageViewerWindow()
    mainWin.setWindowTitle(APPNAME)

    mainWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
