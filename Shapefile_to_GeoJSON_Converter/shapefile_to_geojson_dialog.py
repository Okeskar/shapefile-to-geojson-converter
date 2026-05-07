import os
from qgis.PyQt.QtWidgets import (
    QDialog,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QFileDialog,
    QMessageBox
)
from PyQt5.QtCore import Qt
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsVectorFileWriter
)


class ShapeToGeoJSONDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shapefile to GeoJSON Converter")
        self.resize(420, 460)

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(QLabel("Select layers to convert:"))

        self.layerList = QListWidget()
        self.layout.addWidget(self.layerList)

        self.layout.addWidget(QLabel("Output Folder:"))

        folder_layout = QHBoxLayout()
        self.outputFolder = QLineEdit()
        self.outputFolder.setReadOnly(True)

        self.btnBrowse = QPushButton("Browse")
        folder_layout.addWidget(self.outputFolder)
        folder_layout.addWidget(self.btnBrowse)

        self.layout.addLayout(folder_layout)

        self.btnConvert = QPushButton("Convert to GeoJSON (with Style)")
        self.layout.addWidget(self.btnConvert)

        self.populate_layers()

        self.btnBrowse.clicked.connect(self.browse_folder)
        self.btnConvert.clicked.connect(self.convert_layers)

    def populate_layers(self):
        self.layerList.clear()

        for layer in QgsProject.instance().mapLayers().values():
            if isinstance(layer, QgsVectorLayer):
                item = QListWidgetItem(layer.name())
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Checked)
                item.setData(Qt.UserRole, layer)
                self.layerList.addItem(item)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder"
        )
        if folder:
            self.outputFolder.setText(folder)

    def convert_layers(self):
        output_dir = self.outputFolder.text()

        if not output_dir:
            QMessageBox.warning(
                self,
                "Error",
                "Please select an output folder"
            )
            return

        converted = 0

        for i in range(self.layerList.count()):
            item = self.layerList.item(i)

            if item.checkState() == Qt.Checked:
                layer = item.data(Qt.UserRole)

                # ---- GeoJSON Path ----
                geojson_path = os.path.join(
                    output_dir,
                    f"{layer.name()}.geojson"
                )

                # ---- Export GeoJSON ----
                options = QgsVectorFileWriter.SaveVectorOptions()
                options.driverName = "GeoJSON"
                options.fileEncoding = "UTF-8"

                QgsVectorFileWriter.writeAsVectorFormatV2(
                    layer,
                    geojson_path,
                    QgsProject.instance().transformContext(),
                    options
                )

                # ---- Export QGIS Style (.qml) ----
                style_path = os.path.join(
                    output_dir,
                    f"{layer.name()}.qml"
                )

                layer.saveNamedStyle(style_path)

                converted += 1

        QMessageBox.information(
            self,
            "Completed",
            f"{converted} layer(s) exported with GeoJSON + QML style."
        )
