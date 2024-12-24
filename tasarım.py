from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1760, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Başlık eklemek için QLabel
        self.label_header = QtWidgets.QLabel(self.centralwidget)
        self.label_header.setGeometry(QtCore.QRect(650, 20, 460, 50))  # Konum ve boyut ayarı
        self.label_header.setText("PskManage")  # Başlık metni
        font = QtGui.QFont()  # Yazı tipi ayarı
        font.setPointSize(24)  # Yazı boyutu
        font.setBold(True)  # Kalın yazı
        self.label_header.setFont(font)  # Yazı tipini başlığa uygula
        self.label_header.setAlignment(QtCore.Qt.AlignCenter)  # Başlığı ortala
        self.label_header.setObjectName("label_header")

        # Main Tab Widget
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(20, 80, 1771, 861))
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")

        # Tab 1
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.setupTab1()
        self.tabWidget.addTab(self.tab, "Patients")

        # Tab 2
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.setupTab2()
        self.tabWidget.addTab(self.tab_2, "Notes")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1760, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.initDatabase()
        self.loadPatients()
    
    def initDatabase(self):
        """Initialize the SQLite database."""
        self.connection = sqlite3.connect("patients.db")
        self.cursor = self.connection.cursor()
        
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                last_appointment TEXT NOT NULL,
                next_appointment TEXT NOT NULL,
                diagnosis TEXT,
                current_drugs TEXT,
                drug_history TEXT

            )
            """
        )
        self.connection.commit()

    def loadPatients(self):
        """Load patients from the database into the table widget."""
        self.tableWidget.setRowCount(0)  # Clear the table first
        self.cursor.execute("SELECT name, last_appointment, next_appointment FROM patients")
        for row_data in self.cursor.fetchall():
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            for column, data in enumerate(row_data):
                self.tableWidget.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(data)))

    def setupTab1(self):
        # Title Label
        self.label_title = QtWidgets.QLabel(self.tab)
        self.label_title.setGeometry(QtCore.QRect(340, 200, 251, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_title.setFont(font)
        self.label_title.setObjectName("label_title")
        
        # Table Widget
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(800, 80, 700, 600))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Name-Surname", "Last Appointment", "Next Appointment"])
        header = self.tableWidget.horizontalHeader()
        header.setStretchLastSection(False)  # Disable stretch for the last section (optional)
        for i in range(self.tableWidget.columnCount()):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.cellClicked.connect(self.switch_to_tab2)  # Connect cellClicked to method

        # Form Layout
        self.formLayoutWidget = QtWidgets.QWidget(self.tab)
        self.formLayoutWidget.setGeometry(QtCore.QRect(310, 120, 300, 500))# Form Widget
       
        # Name-Surname Input
        self.lineEdit_name = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_name.setFont(QtGui.QFont("", 13))
        self.lineEdit_name.setPlaceholderText("Enter Name-Surname")
        self.lineEdit_name.setGeometry(QtCore.QRect(0, 150, 300, 40))  # Position and size
        self.lineEdit_name.setObjectName("lineEdit_name")

        # Last Appointment Input
        self.lineEdit_last_appointment = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_last_appointment.setFont(QtGui.QFont("", 13))
        self.lineEdit_last_appointment.setPlaceholderText("Enter Last Appointment")
        self.lineEdit_last_appointment.setGeometry(QtCore.QRect(0, 200, 300, 40))  # Position and size
        self.lineEdit_last_appointment.setObjectName("lineEdit_last_appointment")

        # Next Appointment Input
        self.lineEdit_next_appointment = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_next_appointment.setFont(QtGui.QFont("", 13))
        self.lineEdit_next_appointment.setPlaceholderText("Enter Next Appointment")
        self.lineEdit_next_appointment.setGeometry(QtCore.QRect(0, 250, 300, 40))  # Position and size
        self.lineEdit_next_appointment.setObjectName("lineEdit_next_appointment")

        # Add Button
        self.pushButton_add = QtWidgets.QPushButton(self.tab)
        self.pushButton_add.setGeometry(QtCore.QRect(350, 450, 171, 37))
        self.pushButton_add.setFont(QtGui.QFont("", 14))
        self.pushButton_add.setObjectName("pushButton_add")
        self.pushButton_add.clicked.connect(self.add_patient)  # Connect button to add_patient method

    def add_patient(self):
        """Add patient details to the table and the database."""
        name = self.lineEdit_name.text().strip()
        last_appointment = self.lineEdit_last_appointment.text().strip()
        next_appointment = self.lineEdit_next_appointment.text().strip()

        if not name or not last_appointment or not next_appointment:
            QtWidgets.QMessageBox.warning(self.centralwidget, "Input Error", "Please fill in all fields!")
            return

        try:
            self.cursor.execute(
                "INSERT INTO patients (name, last_appointment, next_appointment) VALUES (?, ?, ?)",
                (name, last_appointment, next_appointment)
            )
            self.connection.commit()

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(name))
            self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(last_appointment))
            self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(next_appointment))

            # Clear input fields
            self.lineEdit_name.clear()
            self.lineEdit_last_appointment.clear()
            self.lineEdit_next_appointment.clear()
        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self.centralwidget, "Database Error", f"Error: {e}")

    def switch_to_tab2(self, row, column):
        """Switch to Tab 2 when a name is clicked."""
        if column == 0:  # Ensure only the Name-Surname column triggers the switch
            name_surname = self.tableWidget.item(row, column).text()
            self.lineEdit_note_name.setText(name_surname)  # Set the name in Tab 2 input
            self.tabWidget.setCurrentIndex(1)  # Switch to Tab 2

    def setupTab2(self):
        self.textEdit_notes = QtWidgets.QTextEdit(self.tab_2)
        self.textEdit_notes.setGeometry(QtCore.QRect(1040, 150, 631, 491))
        self.textEdit_notes.setObjectName("textEdit_notes")

        self.label_notes_title = QtWidgets.QLabel(self.tab_2)
        self.label_notes_title.setGeometry(QtCore.QRect(1080, 100, 251, 51))
        self.label_notes_title.setFont(QtGui.QFont("", 16))
        self.label_notes_title.setObjectName("label_notes_title")

        self.widget_form = QtWidgets.QWidget(self.tab_2)
        self.widget_form.setGeometry(QtCore.QRect(170, 230, 811, 331))
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.widget_form)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(60, 50, 331, 200))
        self.formLayout_2 = QtWidgets.QVBoxLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)

        self.lineEdit_note_name = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_note_name.setFont(QtGui.QFont("", 13))
        self.lineEdit_note_name.setPlaceholderText("Patient Name-Surname")
        self.lineEdit_note_name.setObjectName("lineEdit_note_name")
        self.formLayout_2.addWidget(self.lineEdit_note_name)

        self.lineEdit_note_date = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_note_date.setFont(QtGui.QFont("", 13))
        self.lineEdit_note_date.setObjectName("lineEdit_note_date")
        self.formLayout_2.addWidget(self.lineEdit_note_date)

        self.lineEdit_note_content = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_note_content.setFont(QtGui.QFont("", 13))
        self.lineEdit_note_content.setObjectName("lineEdit_note_content")
        self.formLayout_2.addWidget(self.lineEdit_note_content)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Patient Management System"))
        self.label_title.setText(_translate("MainWindow", "Add New Patient"))
        self.pushButton_add.setText(_translate("MainWindow", "Add"))
        self.label_notes_title.setText(_translate("MainWindow", "My Notes"))
       
# Main Execution
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
