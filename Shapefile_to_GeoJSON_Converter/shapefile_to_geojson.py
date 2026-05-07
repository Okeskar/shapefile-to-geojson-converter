import os
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon
from .shapefile_to_geojson_dialog import ShapeToGeoJSONDialog


class ShapeToGeoJSON:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.action = None

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, 'icon.png')

        self.action = QAction(
            QIcon(icon_path),
            'Shapefile to GeoJSON',
            self.iface.mainWindow()
        )

        self.action.triggered.connect(self.run)

        self.iface.addPluginToMenu(
            '&Shapefile to GeoJSON',
            self.action
        )

        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removePluginMenu(
            '&Shapefile to GeoJSON',
            self.action
        )
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        self.dlg = ShapeToGeoJSONDialog()
        self.dlg.exec_()
