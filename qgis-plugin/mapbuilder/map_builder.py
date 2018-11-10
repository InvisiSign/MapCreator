# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MapBuilder
                                 A QGIS plugin
 This plugin builds an InvisiSign map
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-10-19
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Chris Daley
        email                : chebizarro@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os, sys

from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog, QDialog, QToolButton, QMenu

from qgis.core import QgsVectorLayer, QgsProject

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .map_builder_dialog import MapBuilderDialog
import os.path

protos_path = os.path.join(os.path.dirname(__file__), 'proto')
if protos_path not in sys.path:
    sys.path.append(protos_path)

from .proto_import import parseProtobuf
from .proto_export import NavatarMap

class MapBuilder:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
                
        # initialize plugin directory
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

        # Create the dialog (after translation) and keep reference
        # self.dlg = MapBuilderDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Invisign Map Builder')
        # TODO: We are going to let the user set this up in a future iteration
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

        icon_path = ':/plugins/map_builder/icon.png'
 
        self.add_action(
            ':/plugins/map_builder/import.png',
            text=self.tr(u'Import InvisiSign Map'),
            callback=self.openImport,
            parent=self.iface.mainWindow())

        self.add_action(
            ':/plugins/map_builder/export.png',
            text=self.tr(u'Export InvisiSign Map'),
            callback=self.openExport,
            parent=self.iface.mainWindow())

        menu = QMenu()
        icon = QIcon(icon_path)
        menu.addAction(QAction(icon, self.tr(u'Show Level'), self.iface.mainWindow()))

        tool_button = QToolButton(self.iface.mainWindow())
        tool_button.setMenu(menu)
        tool_button.setIcon(icon)
        tool_button.setPopupMode(QToolButton.InstantPopup)
        self.toolbar.addWidget(tool_button)

    def unload(self):
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
            exporter = NavatarMap()
            exporter.export_map(layers, qfd.selectedFiles()[0])
