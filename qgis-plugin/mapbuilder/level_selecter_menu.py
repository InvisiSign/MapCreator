# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LevelSelecterMenu
                                 A QGIS plugin
 This plugin builds a Reference Point Navigation map
                             -------------------
        begin                : 2018-10-19
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Chris Daley
        email                : chebizarro@gmail.com
 ***************************************************************************/
"""

from PyQt5 import QtWidgets


class LevelSelecterMenu(QtWidgets.QMenu):
    def __init__(self, layers, parent=None):
        super(LevelSelecterMenu, self).__init__(parent)
        self.layers = layers
        self.buildLevelMenu()

    def layerChanged(self, layer):
        self.active_layer = layer
        self.clear()
        if layer not in self.levels:
            if type(layer) == QgsVectorLayer:
                self.addLayer(layer)
            else:
                return
        for action in self.levels[layer]:
            self.addAction(action)

    def showAllAction(self):
        self.show_all_action = QAction(u'Show all', self.parent)
        self.show_all_action.triggered.connect(lambda b: self.active_layer.setSubsetString(None))

    def buildLevelMenu(self):
        #layers = [layer for name, layer in QgsProject.instance().mapLayers().items() if type(layer) == QgsVectorLayer]
        self.levels = {}
        for layer in self.layers:
            self.addLayer(layer)

    def addLayer(self, layer):
        layer.setSubsetString(None)
        levels = self.buildLevelSet(layer)
        self.levels[layer] = []
        for level in levels:
            action = QAction(level, self.parent)
            action.triggered.connect(lambda b, ly=layer, l=level: self.levelSelected(ly, l))
            self.addAction(action)
            self.levels[layer].append(action)
        self.levels[layer].append(self.show_all_action)
    
    def levelSelected(self, layer, level):
        layer.setSubsetString(None)
        layer.setSubsetString('"level"=\'{}\''.format(level))
        layer.updateExtents(True)

    def buildLevelSet(self, layer):
        query = '"level"<> \'NULL\''
        selection = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
        return sorted(set([feature["level"] for feature in selection]))

