from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
import sqlite3

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

class LoginRegisterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kullanıcı Kayıt ve Giriş")
        self.setGeometry(200, 200, 1960, 400)
        self.initDatabase()
        self.main_window = None
        
        self.layout = QVBoxLayout()
        
        # Kullanıcı adı ve şifre alanları
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Kullanıcı Adı")
        self.layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)
        
        # Kayıt ve giriş butonları
        self.register_button = QPushButton("Kayıt Ol", self)
        self.register_button.clicked.connect(self.register_user)
        self.layout.addWidget(self.register_button)
        
        self.login_button = QPushButton("Giriş Yap", self)
        self.login_button.clicked.connect(self.login_user)
        self.layout.addWidget(self.login_button)
        
        # Sonuçları göstermek için bir etiket
        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)
        
        self.setLayout(self.layout)
    
    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username and password:
            connection = sqlite3.connect("users.db")
            cursor = connection.cursor()
            
            try:
                cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
                connection.commit()
                QMessageBox.information(self, "Başarılı", "Kayıt işlemi tamamlandı.")
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Hata", "Bu kullanıcı adı zaten alınmış.")
            finally:
                connection.close()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")
    
    def login_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username and password:
            connection = sqlite3.connect("users.db")
            cursor = connection.cursor()
            
            cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            
            if user:
                QMessageBox.information(self, "Başarılı", "Giriş başarılı! Hoşgeldiniz.")
            
                # Ana pencereyi başlat
                self.main_window = QtWidgets.QMainWindow()
                self.ui = Ui_MainWindow()
                self.ui.setupUi(self.main_window)
                
                # Login penceresini kapat ve ana pencereyi göster
                self.close()
                self.main_window.show()

            else:
                QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre yanlış.")
            
            connection.close()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")

    def initDatabase(self):
        """Veritabanını başlat ve gerekli tabloları oluştur."""
        connection = sqlite3.connect("users.db")  # Kullanıcı veritabanına bağlan
        cursor = connection.cursor()

        # User tablosunu oluştur
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()

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
                drug_history TEXT,
                my_notes TEXT
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
        self.label_title.setGeometry(QtCore.QRect(330, 220, 251, 61))
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
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.DoubleClicked)  # Enable editing
        self.tableWidget.itemChanged.connect(self.update_patient_data)  # Connect to update method

        for i in range(self.tableWidget.columnCount()):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.cellClicked.connect(self.switch_to_tab2)  # Connect cellClicked to method

        # Form Layout
        self.formLayoutWidget = QtWidgets.QWidget(self.tab)
        self.formLayoutWidget.setGeometry(QtCore.QRect(180, 300, 500, 500))# Form Widget
        self.formLayoutWidget.setObjectName("formLayoutWidget")

        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        
        # Name-Surname Input
        self.label_name = QtWidgets.QLabel("Name-Surname:")
        self.label_name.setFont(QtGui.QFont("", 12))
        self.lineEdit_name = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_name.setFont(QtGui.QFont("", 13))
        
        self.formLayout.addRow(self.label_name, self.lineEdit_name)

        # Last Appointment Input
        self.label_last_appointment = QtWidgets.QLabel("Last Appointment:")
        self.lineEdit_last_appointment = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_last_appointment.setFont(QtGui.QFont("", 13))
        self.label_last_appointment.setFont(QtGui.QFont("", 12))
        
        self.lineEdit_last_appointment.setGeometry(QtCore.QRect(0, 200, 300, 40))  # Position and size
        self.lineEdit_last_appointment.setObjectName("lineEdit_last_appointment")
        self.formLayout.addRow(self.label_last_appointment, self.lineEdit_last_appointment)
        # Next Appointment Input
        self.label_next_appointment = QtWidgets.QLabel("Next Appointment:")
        self.label_next_appointment.setFont(QtGui.QFont("", 12))
        self.lineEdit_next_appointment = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_next_appointment.setFont(QtGui.QFont("", 13))
        
        self.lineEdit_next_appointment.setGeometry(QtCore.QRect(0, 250, 300, 40))  # Position and size
        self.lineEdit_next_appointment.setObjectName("lineEdit_next_appointment")
        self.formLayout.addRow(self.label_next_appointment, self.lineEdit_next_appointment)
        # Add Button
        self.pushButton_add = QtWidgets.QPushButton(self.tab)
        self.pushButton_add.setGeometry(QtCore.QRect(370, 450, 171, 37))
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

    def update_patient_data(self, item):
        """Update the patient data in the database when a cell is edited."""
        row = item.row()
        column = item.column()
        new_value = item.text()

        # Check which column was edited
        if column in (1, 2):  # Only update for Last or Next Appointment
            try:
                # Get the patient's name to identify the record
                name = self.tableWidget.item(row, 0).text()

                # Determine the column name to update
                column_name = "last_appointment" if column == 1 else "next_appointment"

                # Update the database
                self.cursor.execute(
                    f"UPDATE patients SET {column_name} = ? WHERE name = ?",
                    (new_value, name)
                )
                self.connection.commit()
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
        self.textEdit_notes.setGeometry(QtCore.QRect(900, 150, 631, 491))
        self.textEdit_notes.setObjectName("textEdit_notes")
        
        # Notes Title Label
        self.label_notes_title = QtWidgets.QLabel(self.tab_2)
        self.label_notes_title.setGeometry(QtCore.QRect(200, 200, 351, 51))
        self.label_notes_title.setFont(QtGui.QFont("", 22))
        self.label_notes_title.setText("Patient")  # Başlık olarak "Patients" ekledik
        self.label_notes_title.setObjectName("label_notes_title")

        self.label_notes_title = QtWidgets.QLabel(self.tab_2)
        self.label_notes_title.setGeometry(QtCore.QRect(1080, 100, 351, 51))
        self.label_notes_title.setFont(QtGui.QFont("", 16))
        self.label_notes_title.setObjectName("label_notes_title")

        self.widget_form = QtWidgets.QWidget(self.tab_2)
        self.widget_form.setGeometry(QtCore.QRect(170, 230, 811, 331))
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.widget_form)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(30, 50, 500, 200))
        self.formLayout_2 = QtWidgets.QVBoxLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)

        # Name-Surname Input and Label
        h_layout_name = QtWidgets.QHBoxLayout()
        self.label_note_name = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_note_name.setFont(QtGui.QFont("", 12))
        self.label_note_name.setText("Name-Surname: ")
        h_layout_name.addWidget(self.label_note_name)

        self.lineEdit_note_name = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_note_name.setFont(QtGui.QFont("", 13))        
        self.lineEdit_note_name.setObjectName("lineEdit_note_name")
        self.lineEdit_note_name.textChanged.connect(self.load_patient_data)  # Load data on name change
        h_layout_name.addWidget(self.lineEdit_note_name)
        
        self.formLayout_2.addLayout(h_layout_name)

        # Diagnosis Input and Label
        h_layout_diagnosis = QtWidgets.QHBoxLayout()
        self.label_note_diagnosis = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_note_diagnosis.setFont(QtGui.QFont("", 12))
        self.label_note_diagnosis.setText("Diagnosis")
        h_layout_diagnosis.addWidget(self.label_note_diagnosis)

        self.lineEdit_note_diagnosis = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_note_diagnosis.setFont(QtGui.QFont("", 13))
        self.lineEdit_note_diagnosis.setObjectName("lineEdit_note_diagnosis")
        h_layout_diagnosis.addWidget(self.lineEdit_note_diagnosis)
        
        self.formLayout_2.addLayout(h_layout_diagnosis)
        
        # Current Drugs Input and Label
        h_layout_drugs = QtWidgets.QHBoxLayout()
        self.label_note_current_drugs = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_note_current_drugs.setFont(QtGui.QFont("", 12))
        self.label_note_current_drugs.setText("Current Drugs")
        h_layout_drugs.addWidget(self.label_note_current_drugs)

        self.lineEdit_note_current_drugs = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_note_current_drugs.setFont(QtGui.QFont("", 13))
        self.lineEdit_note_current_drugs.setObjectName("lineEdit_note_current_drugs")
        h_layout_drugs.addWidget(self.lineEdit_note_current_drugs)
        
        self.formLayout_2.addLayout(h_layout_drugs)

        # Drug History Input and Label
        h_layout_history = QtWidgets.QHBoxLayout()
        self.label_note_drug_history = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_note_drug_history.setFont(QtGui.QFont("", 12))
        self.label_note_drug_history.setText("Drug History")
        h_layout_history.addWidget(self.label_note_drug_history)

        self.lineEdit_note_drug_history = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.lineEdit_note_drug_history.setFont(QtGui.QFont("", 13))
        self.lineEdit_note_drug_history.setObjectName("lineEdit_note_drug_history")
        h_layout_history.addWidget(self.lineEdit_note_drug_history)
        
        self.formLayout_2.addLayout(h_layout_history)
        
        # Kaydet Butonu
        self.save_button = QtWidgets.QPushButton(self.tab_2)
        self.save_button.setGeometry(QtCore.QRect(390, 520, 200, 40))  # Butonun boyutları ve konumu
        self.save_button.setText("Kaydet")  # Buton metni
        self.save_button.setFont(QtGui.QFont("", 12))  # Buton fontu
        # self.save_button.setEnabled(False)  # Butonun işlevsizlik durumuna getirilmesi
        self.save_button.clicked.connect(self.save_notes)  # Connect save button to save_notes method

    def save_notes(self):
        """Save or update patient notes in the database."""
        name = self.lineEdit_note_name.text().strip()
        diagnosis = self.lineEdit_note_diagnosis.text().strip()
        current_drugs = self.lineEdit_note_current_drugs.text().strip()
        my_notes = self.textEdit_notes.toPlainText().strip()

        if not name:
            QtWidgets.QMessageBox.warning(self.centralwidget, "Input Error", "Please enter the patient's name!")
            return

        try:
            # Check if the patient exists
            self.cursor.execute(
                "SELECT diagnosis, current_drugs, drug_history, my_notes FROM patients WHERE name = ?",
                (name,)
            )
            existing_data = self.cursor.fetchone()

            if existing_data:
                # Handle updates
                existing_diagnosis, existing_current_drugs, existing_drug_history, existing_my_notes = existing_data

                # Update diagnosis only if it is new and different
                if diagnosis and diagnosis != existing_diagnosis:
                    existing_diagnosis = diagnosis

                # Manage current and history drugs
                if existing_current_drugs and existing_current_drugs != current_drugs:
                    # Move the old current_drugs to drug_history
                    if existing_drug_history:
                        drug_history = f"{existing_drug_history}\n{existing_current_drugs}"
                    else:
                        drug_history = existing_current_drugs
                else:
                    drug_history = existing_drug_history

                # Update my_notes only with new additions
                if my_notes and (not existing_my_notes or my_notes not in existing_my_notes):
                    new_note = my_notes.replace(existing_my_notes, "").strip() if existing_my_notes else my_notes
                    my_notes = f"{existing_my_notes}\n{new_note}" if existing_my_notes else new_note
                else:
                    my_notes = existing_my_notes

                # Update the patient record
                self.cursor.execute(
                    """
                    UPDATE patients SET diagnosis = ?, current_drugs = ?, drug_history = ?, my_notes = ? WHERE name = ?
                    """,
                    (existing_diagnosis, current_drugs, drug_history, my_notes, name),
                )
            else:
                # Insert new patient data
                self.cursor.execute(
                    """
                    INSERT INTO patients (name, diagnosis, current_drugs, drug_history, my_notes) VALUES (?, ?, ?, ?, ?)
                    """,
                    (name, diagnosis, current_drugs, "", my_notes),
                )

            self.connection.commit()

            self.load_patient_data()

            # Clear input fields (optional)
            QtWidgets.QMessageBox.information(self.centralwidget, "Success", "Notes saved successfully!")

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self.centralwidget, "Database Error", f"Error: {e}")

    def load_patient_data(self):
        """Load patient data into input fields based on the name."""
        name = self.lineEdit_note_name.text().strip()

        if not name:
            self.lineEdit_note_diagnosis.clear()
            self.lineEdit_note_current_drugs.clear()
            self.lineEdit_note_drug_history.clear()
            self.textEdit_notes.clear()
            return

        try:
            self.cursor.execute(
                "SELECT diagnosis, current_drugs, drug_history, my_notes FROM patients WHERE name = ?",
                (name,)
            )
            patient_data = self.cursor.fetchone()

            if patient_data:
                diagnosis, current_drugs, drug_history, my_notes = patient_data
                self.lineEdit_note_diagnosis.setText(diagnosis if diagnosis else "")
                self.lineEdit_note_current_drugs.setText(current_drugs if current_drugs else "")
                self.lineEdit_note_drug_history.setText(drug_history if drug_history else "")
                self.textEdit_notes.setText(my_notes if my_notes else "")
                QtWidgets.QMessageBox.information(self.centralwidget, "Data Loaded", "Patient data loaded successfully!")
            else:
                self.lineEdit_note_diagnosis.clear()
                self.lineEdit_note_current_drugs.clear()
                self.lineEdit_note_drug_history.clear()
                self.textEdit_notes.clear()
                QtWidgets.QMessageBox.information(self.centralwidget, "No Data", "No data found for the entered patient name.")

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self.centralwidget, "Database Error", f"Error: {e}")

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
    app.setStyle("Fusion")
    login_window = LoginRegisterApp()
    login_window.show()
    sys.exit(app.exec_())
