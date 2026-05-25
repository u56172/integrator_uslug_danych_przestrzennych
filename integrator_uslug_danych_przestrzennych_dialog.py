# -*- coding: utf-8 -*-
import os
import sys
from typing import Dict, List

from qgis.PyQt import QtWidgets
from qgis.PyQt import uic
from qgis.PyQt.QtCore import QSortFilterProxyModel, Qt
from qgis.PyQt.QtGui import QShowEvent, QStandardItem, QStandardItemModel
from .api.region_fetch import RegionFetch
from .api.country_urls_fetcher import CountryUrlsFetcher
from .api.services_urls_fetcher import ServicesUrlsFetcher
from .constants import RADIOBUTTONS_SERVICES
from .utils import QtCompat, MessageUtils

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'integrator_uslug_danych_przestrzennych_dialog_base.ui'))
    
class IntegratorUslugPrzestrzennychDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(IntegratorUslugPrzestrzennychDialog, self).__init__(parent)
        self.setupUi(self)
        self.country_urls_fetcher = CountryUrlsFetcher()
        self.urls_fetcher = ServicesUrlsFetcher()
        self.RegionFetch = None
        self.current_teryt = 'PL'
        self.is_table_empty = True
        try:
            self.RegionFetch = RegionFetch()
        except Exception as e:
            MessageUtils.logWarning(
                f"Brak połączenia z Internetem. Spróbuj ponownie później. Exception: {e}"
            )
            self.RegionFetch = None
        self.country_services_cache: List[Dict[str, str]] = []
        self.setupDialog()
        self.setupVoivodeshipComboBox()
        self.setupSignals()
        self.setupTable()

    def setupDialog(self) -> None:
        self.img_main.setMargin(9)

    def setupSignals(self) -> None:
        for obj in RADIOBUTTONS_SERVICES:
            widget_obj = getattr(self, obj)
            widget_obj.toggled.connect(self.setupTable)
        self.comboBox_voivodeship.currentTextChanged.connect(self.serveVoivodeshipComboBox)
        self.comboBox_county.currentTextChanged.connect(self.serveCountyComboBox)
        self.comboBox_commune.currentTextChanged.connect(self.serveCommuneComboBox)
        self.search_lineedit.textChanged.connect(self.applySearchFilter)

    def setupVoivodeshipComboBox(self):
        self.comboBox_voivodeship.clear()
        self.comboBox_voivodeship.addItem('--- usługi dla całego kraju ---')
        self.comboBox_voivodeship.setItemData(0, 'PL')
        self.comboBox_voivodeship.setCurrentIndex(0)
        if self.RegionFetch:
            self._fillComboBox(self.comboBox_voivodeship, self.RegionFetch.getVoivodeships())
        else:
            MessageUtils.logWarning("Brak połączenia z Internetem. Spróbuj ponownie później")
        
    def serveVoivodeshipComboBox(self):
        current_idx = self.comboBox_voivodeship.currentIndex()
        self._updateTerytAndTable(self.comboBox_voivodeship.itemData(current_idx))
        self.setupCountyComboBox(int(current_idx))

    def setupCountyComboBox(self, current_idx : int):
        self.comboBox_county.clear()
        self.comboBox_commune.clear()
        if current_idx < 1:
            return
        if self.RegionFetch:
            self.comboBox_county.addItem('--- usługi dla całego województwa ---')
            self.comboBox_county.setItemData(0, self.current_teryt[:2])
            self._fillComboBox(self.comboBox_county, self.RegionFetch.getCountiesByTeryt(self.current_teryt))
        else:
            MessageUtils.logWarning("Brak połączenia z Internetem. Spróbuj ponownie później")

    def serveCountyComboBox(self):
        current_idx = self.comboBox_county.currentIndex()
        self._updateTerytAndTable(self.comboBox_county.itemData(current_idx))
        self.setupCommuneComboBox(current_idx)

    def setupCommuneComboBox(self, current_idx : int):
        self.comboBox_commune.clear()
        if current_idx < 1:
            return
        if self.RegionFetch:
            self.comboBox_commune.addItem('--- usługi dla całego powiatu ---')
            self.comboBox_commune.setItemData(0, self.current_teryt[:4])
            self._fillComboBox(self.comboBox_commune,self.RegionFetch.getCommunesByTeryt(self.current_teryt))
        else:
            MessageUtils.logWarning("Brak połączenia z Internetem. Spróbuj ponownie później")

    def serveCommuneComboBox(self):
        current_idx = self.comboBox_commune.currentIndex()  
        self._updateTerytAndTable(self.comboBox_commune.itemData(current_idx))

    def _updateTerytAndTable(self, teryt : str):
        " Podmienia aktualny teryt na nową wartość i aktualizuje tablicę, jeśli nastąpiła zmiana "
        if self.current_teryt == teryt or teryt == None:
            return
        self.current_teryt = teryt
        MessageUtils.logInfo(f"Pobieranie usług dla terytu: {self.current_teryt}")
        self.setupTable()

    def _fillComboBox(self, comboBox, region_dict : dict):
        comboBox.addItems(region_dict.values())
        for idx, teryt in enumerate(region_dict.keys(), start=1):
            comboBox.setItemData(idx, teryt)
        comboBox.setCurrentIndex(0)

    def setupTable(self) -> None:
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Nazwa usługi', 'Adres usługi'])
        self.fillServicesTable()
        self.configureTableHeader()
        self.setupSearch()
        self.applySearchFilter(self.search_lineedit.text())

    def configureTableHeader(self) -> None:
        resize_interactive = QtCompat.getEnum(QtWidgets.QHeaderView, 'ResizeMode', 'Interactive')
        header = self.services_table.horizontalHeader()
        header.setSectionResizeMode(0, resize_interactive)
        self.services_table.setColumnWidth(0, 400)
        header.setSectionResizeMode(1, resize_interactive)
        self.services_table.setColumnWidth(1, 300)
        self.services_table.setVerticalHeader(self.services_table.verticalHeader().setDefaultSectionSize(14))
        ascending = QtCompat.getEnum(Qt, 'SortOrder', 'AscendingOrder')
        self.services_table.horizontalHeader().setSortIndicator(0, ascending)
        self.services_table.setSortingEnabled(True)
        header = self.services_table.verticalHeader()
        align_center = QtCompat.getEnum(Qt, 'AlignmentFlag', 'AlignCenter')
        header.setDefaultAlignment(align_center)

    def fillServicesTable(self) -> None:
        serv_rows = self.urls_fetcher.fetchUrls(self.current_teryt, self.getSelectedServiceType())
        for service_row in serv_rows:
            row = [
                QStandardItem(service_row['dataset_name']),
                QStandardItem(service_row['url']),
            ]
            self.model.appendRow(row)
        if len(serv_rows) == 0:
            self.is_table_empty = True
            row = [
                QStandardItem("Aktualnie brak usług dla danego obszaru. Wybierz inny obszar lub rodzaj usługi..."),
                QStandardItem("")
            ]
            self.model.appendRow(row)
        else:
            self.is_table_empty = False
            
        self.services_table.setModel(self.model)

    def setupSearch(self) -> None:
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(0)
        self.services_table.setModel(self.proxy_model)

    def applySearchFilter(self, text: str) -> None:
        case_insensitive = QtCompat.getEnum(Qt, 'CaseSensitivity', 'CaseInsensitive')
        self.proxy_model.setFilterCaseSensitivity(case_insensitive)
        self.proxy_model.setFilterFixedString(text)

    def getSelectedServiceType(self) -> str:
        if self.wmts_rdbtn.isChecked():
            return 'WMTS'
        if self.wcs_rdbtn.isChecked():
            return 'WCS'
        if self.wfs_rdbtn.isChecked():
            return 'WFS'
        return 'WMS'

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        # self.country_services_cache = self.country_urls_fetcher.fetchCountryUrls()
        self.setupTable()
        self.wms_rdbtn.setFocus()

    def closeEvent(self, event: QShowEvent) -> None:
        event.accept()
        self.accept()

