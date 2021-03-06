# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MapBuilder
                                 A QGIS plugin
 This plugin builds a Reference Point Navigation map
                              -------------------
        begin                : 2018-10-19
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Chris Daley
        email                : chebizarro@gmail.com
 ***************************************************************************/
"""
import os, sys

from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QActionGroup, QFileDialog, QDialog, QToolButton, QMenu

from qgis.core import QgsVectorLayer, QgsProject, QgsFeatureRequest

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
import os.path

protos_path = os.path.join(os.path.dirname(__file__), 'proto')
if protos_path not in sys.path:
    sys.path.append(protos_path)

from .proto_import import parseProtobuf
from .proto_export import RPNMap


class MapBuilder:
    """QGIS Plugin Implementation."""
    def __init__(self, iface):
        """Constructor.
        :param iface: A QGIS interface instance
        :type iface: QgsInterface
        """
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'MapBuilder_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Invisign Map Builder')
        self.toolbar = self.iface.addToolBar(u'MapBuilder')
        self.toolbar.setObjectName(u'MapBuilder')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('MapBuilder', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        self.add_action(
            ':/plugins/map_builder/resources/import.svg',
            text=self.tr(u'Import Navatar Map'),
            callback=self.openImport,
            parent=self.iface.mainWindow())

        self.add_action(
            ':/plugins/map_builder/resources/export.svg',
            text=self.tr(u'Export Navatar Map'),
            callback=self.openExport,
            parent=self.iface.mainWindow())

        self.show_all_action = QAction('Show all', self.iface.mainWindow())
        self.show_all_action.setCheckable(True)
        self.show_all_action.triggered.connect(lambda b: self.iface.activeLayer().setSubsetString(None))

        self.add_action(
            ':/plugins/map_builder/resources/floor.svg',
            text=self.tr(u'Add Navigable Space'),
            callback=self.openExport,
            parent=self.iface.mainWindow())

        self.add_action(
            ':/plugins/map_builder/resources/landmark.svg',
            text=self.tr(u'Add Landmark'),
            callback=self.openExport,
            parent=self.iface.mainWindow())

        self.setUpLevelMenu()

        
    def setUpLevelMenu(self):
        self.level_menu = QMenu()
        icon = QIcon(':/plugins/map_builder/resources/floors.svg')
        self.iface.currentLayerChanged.connect(self.layerChanged)
        self.level_menu_button = QToolButton(self.iface.mainWindow())
        self.level_menu_button.setMenu(self.level_menu)
        self.level_menu_button.setIcon(icon)
        self.level_menu_button.setPopupMode(QToolButton.InstantPopup)
        self.buildLevelMenu()
        self.toolbar.addWidget(self.level_menu_button)

    def layerChanged(self, layer):
        self.level_menu.clear()
        if layer not in self.level_data:
            self.level_menu_button.setEnabled(False)
            return
        self.level_menu_button.setEnabled(True)
        for action in self.level_data[layer].actions():
            self.level_menu.addAction(action)
        self.level_menu.addAction(self.show_all_action)
        self.level_data[layer].addAction(self.show_all_action)


    def buildLevelMenu(self):
        layers = [layer for name, layer in QgsProject.instance().mapLayers().items() if type(layer) == QgsVectorLayer]
        self.level_data = {}
        for layer in layers:
            layer.setSubsetString(None)
            levels = self.buildLevelSet(layer)
            group = QActionGroup(self.iface.mainWindow())
            self.level_data[layer] = group
            for level in levels:
                action = QAction(level, self.iface.mainWindow())
                action.setCheckable(True)
                action.triggered.connect(lambda b, ly=layer, l=level: self.levelSelected(ly, l))
                self.level_menu.addAction(action)
                group.addAction(action)
    
    def levelSelected(self, layer, level):
        layer.setSubsetString(None)
        layer.setSubsetString('"level"=\'{}\''.format(level))
        layer.updateExtents(True)

    def buildLevelSet(self, layer):
        query = '"level"<> \'NULL\''
        selection = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        return sorted(set([feature["level"] for feature in selection]))


    def unload(self):
        """Disconnect the LayerChanged Signal"""
        self.iface.currentLayerChanged.disconnect()

        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Invisign Map Builder'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        # self.dlg.show()
        # Run the dialog event loop
        # result = self.dlg.exec_()
        # See if OK was pressed
        #if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
        pass

    def openImport(self):
        qfd = QFileDialog()
        title = 'Open File'
        f = QFileDialog.getOpenFileName(qfd, title, "~")
        if len(f[0]) > 2:
            parseProtobuf(f[0])

    def openExport(self):
        qfd = QFileDialog()
        qfd.setFileMode(QFileDialog.DirectoryOnly)
        title = 'Select Directory'
        if qfd.exec_() == QDialog.Accepted:
            layers = [layer for name, layer in QgsProject.instance().mapLayers().items() if type(layer) == QgsVectorLayer]
            exporter = RPNMap()
            exporter.export_map(layers, qfd.selectedFiles()[0])
