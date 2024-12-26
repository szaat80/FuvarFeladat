from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QWidget, QFormLayout,
    QLineEdit, QSpinBox, QPushButton, QHBoxLayout,
    QTableWidget, QTabWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt
import sqlite3

class DatabaseManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.conn = sqlite3.connect('fuvarok.db')
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Törzsadat Kezelő")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        
        layout = QVBoxLayout()
        
        # Tab widget létrehozása
        tabs = QTabWidget()
        tabs.addTab(self.createFactoriesTab(), "Gyárak")
        tabs.addTab(self.createAddressesTab(), "Címek")
        tabs.addTab(self.createZonesTab(), "Övezetek")
        layout.addWidget(tabs)
        
        self.setLayout(layout)

    def createFactoriesTab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Adatbeviteli mezők
        form_layout = QFormLayout()
        self.factory_name = QLineEdit()
        self.factory_price = QSpinBox()
        self.factory_price.setRange(0, 1000000)
        form_layout.addRow("Gyár neve:", self.factory_name)
        form_layout.addRow("Fuvardíj:", self.factory_price)
        
        # Gombok
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Hozzáadás")
        add_btn.clicked.connect(self.addFactory)
        delete_btn = QPushButton("Törlés")
        delete_btn.clicked.connect(self.deleteFactory)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(delete_btn)
        
        # Táblázat
        self.factory_table = QTableWidget()
        self.factory_table.setColumnCount(3)
        self.factory_table.setHorizontalHeaderLabels(["ID", "Név", "Fuvardíj"])
        
        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.factory_table)
        widget.setLayout(layout)
        
        self.loadFactories()
        return widget

    def createAddressesTab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        self.address = QLineEdit()
        self.address_price = QSpinBox()
        self.address_price.setRange(0, 1000000)
        form_layout.addRow("Cím:", self.address)
        form_layout.addRow("Egyedi ár:", self.address_price)
        
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Hozzáadás")
        add_btn.clicked.connect(self.addAddress)
        delete_btn = QPushButton("Törlés")
        delete_btn.clicked.connect(self.deleteAddress)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(delete_btn)
        
        self.address_table = QTableWidget()
        self.address_table.setColumnCount(3)
        self.address_table.setHorizontalHeaderLabels(["ID", "Cím", "Ár"])
        
        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.address_table)
        widget.setLayout(layout)
        
        self.loadAddresses()
        return widget

    def createZonesTab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        self.zone_name = QLineEdit()
        self.zone_price = QSpinBox()
        self.zone_price.setRange(0, 1000000)
        form_layout.addRow("Övezet:", self.zone_name)
        form_layout.addRow("Alapdíj:", self.zone_price)
        
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Hozzáadás")
        add_btn.clicked.connect(self.addZone)
        delete_btn = QPushButton("Törlés")
        delete_btn.clicked.connect(self.deleteZone)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(delete_btn)
        
        self.zone_table = QTableWidget()
        self.zone_table.setColumnCount(3)
        self.zone_table.setHorizontalHeaderLabels(["ID", "Név", "Alapdíj"])
        
        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.zone_table)
        widget.setLayout(layout)
        
        self.loadZones()
        return widget

    def addFactory(self):
        name = self.factory_name.text()
        price = self.factory_price.value()
        if name and price:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO factories (nev, fuvardij) VALUES (?, ?)", (name, price))
            self.conn.commit()
            self.loadFactories()
            self.factory_name.clear()
            self.factory_price.setValue(0)

    def addAddress(self):
        address = self.address.text()
        price = self.address_price.value()
        if address and price:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO addresses (cim, ar) VALUES (?, ?)", (address, price))
            self.conn.commit()
            self.loadAddresses()
            self.address.clear()
            self.address_price.setValue(0)

    def addZone(self):
        name = self.zone_name.text()
        price = self.zone_price.value()
        if name and price:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO zones (nev, alapdij) VALUES (?, ?)", (name, price))
            self.conn.commit()
            self.loadZones()
            self.zone_name.clear()
            self.zone_price.setValue(0)

    def deleteFactory(self):
        selected = self.factory_table.selectedItems()
        if selected:
            row = selected[0].row()
            id_item = self.factory_table.item(row, 0)
            if id_item:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM factories WHERE id=?", (id_item.text(),))
                self.conn.commit()
                self.loadFactories()

    def deleteAddress(self):
        selected = self.address_table.selectedItems()
        if selected:
            row = selected[0].row()
            id_item = self.address_table.item(row, 0)
            if id_item:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM addresses WHERE id=?", (id_item.text(),))
                self.conn.commit()
                self.loadAddresses()

    def deleteZone(self):
        selected = self.zone_table.selectedItems()
        if selected:
            row = selected[0].row()
            id_item = self.zone_table.item(row, 0)
            if id_item:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM zones WHERE id=?", (id_item.text(),))
                self.conn.commit()
                self.loadZones()

    def loadFactories(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM factories")
        self.factory_table.setRowCount(0)
        for row, data in enumerate(cursor.fetchall()):
            self.factory_table.insertRow(row)
            for col, item in enumerate(data):
                self.factory_table.setItem(row, col, QTableWidgetItem(str(item)))

    def loadAddresses(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM addresses")
        self.address_table.setRowCount(0)
        for row, data in enumerate(cursor.fetchall()):
            self.address_table.insertRow(row)
            for col, item in enumerate(data):
                self.address_table.setItem(row, col, QTableWidgetItem(str(item)))

    def loadZones(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM zones")
        self.zone_table.setRowCount(0)
        for row, data in enumerate(cursor.fetchall()):
            self.zone_table.insertRow(row)
            for col, item in enumerate(data):
                self.zone_table.setItem(row, col, QTableWidgetItem(str(item)))