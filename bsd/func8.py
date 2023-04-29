from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QComboBox, QTableWidget, QTableWidgetItem, QListWidget, QAbstractItemView, QListWidgetItem
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import mysql.connector

class AuthenticationWindow(QWidget):
    def __init__(self):
        super().__init__()

        # establecer la conexión con la base de datos MySQL usando mysql.connector
        self.cnx = mysql.connector.connect(user='proot', password='Prootproot1!',
                              host='3.13.64.84',
                              database='gestionuniversidad')
        # Credenciales del cliente
        self.client_secrets_file = 'client_secrets.json'
        
        # Botón de autenticación de Google
        self.google_auth_button = QPushButton('Ingresar con Google')
        self.google_auth_button.clicked.connect(self.authenticate_with_google)
        # Botón de cierre de sesión
        self.logout_button = QPushButton('Cerrar sesión')
        self.logout_button.clicked.connect(self.logout)
        self.logout_button.hide()

        # Label de estado
        self.status_label = QLabel('')
        
        # ComboBox de seccion, alumnos, nota
        self.seccion_combo_box = QComboBox()
        self.seccion_combo_box.hide()
        self.alumno_combo_box = QComboBox()
        self.alumno_combo_box.hide()
        #self.nota_combo_box = QComboBox()
        #self.nota_combo_box.hide()

	#TableList de Fases con practica y teoria
        self.table_list_widget = QTableWidget(10,10)
        self.table_list_widget.hide()
        self.table0_list_widget = QListWidget()
        self.table0_list_widget.hide()
        self.table1_list_widget = QListWidget()
        self.table1_list_widget.hide()
        self.table2_list_widget = QListWidget()
        self.table2_list_widget.hide()

        # Diseño de la ventana
        layout = QVBoxLayout()
        layout.addWidget(self.google_auth_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.logout_button)
        layout.addWidget(self.seccion_combo_box)
        layout.addWidget(self.alumno_combo_box)
        #layout.addWidget(self.nota_combo_box)
        layout.addWidget(self.table_list_widget)
        layout.addWidget(self.table0_list_widget)
        layout.addWidget(self.table1_list_widget)
        layout.addWidget(self.table2_list_widget)
        
        self.setLayout(layout)
        self.show()
        print("HOLA")
        # Habilitar edición al hacer doble clic o seleccionar
        self.table_list_widget.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        self.table0_list_widget.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        self.table1_list_widget.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        #self.table2_list_widget.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        

    def logout(self):
        codigo_per=0
        # mostrar el ComboBox
        self.seccion_combo_box.hide()
        self.alumno_combo_box.hide()
        self.table_list_widget.hide()
        self.logout_button.hide()

    def authenticate_with_google(self):

        # Conectar señal de cambio de índice de ComboBox
        self.seccion_combo_box.currentIndexChanged.connect(self.update_alumno_combo_box)
        #self.alumno_combo_box.currentIndexChanged.connect(self.update_nota_combo_box)

        
        result = True
        if result:
            codigo_per = 31002
            # actualizar la lista de alumnos
            self.seccion_combo_box.clear()
            self.alumno_combo_box.clear()
            self.seccion_combo_box.addItems(self.get_secciones(codigo_per))
            #Codigos de secciones combobox
            self.get_secciones6(60001)
            #self.alumno_combo_box.addItems(self.get_secciones6(60001))

            self.alumno_combo_box.addItems(self.get_secciones0())
            #self.nota_combo_box.addItems(self.get_secciones1(10001,30001))
        


            # mostrar el ComboBox
            self.seccion_combo_box.show()
            self.alumno_combo_box.show()
            self.table_list_widget.show()
            self.logout_button.show()

        else:
            print('No está registrado en el sistema, su correo no esta vinculado a ninguna cuenta')
    def get_secciones(self, codigo):
        """Obtener una lista de los nombres de los alumnos en la base de datos."""
        cursor = self.cnx.cursor()
        #cursor.execute('SELECT seccion FROM Clase WHERE cod_docente = %s', (codigo,))
        cursor.execute('SELECT codigo FROM Clase WHERE cod_docente = %s', (codigo,))
        alumnos = []
        for seccion in cursor:
            alumnos.append(str(seccion[0]))
        return alumnos

    def get_secciones0(self):
        """Obtener una lista de los nombres de los alumnos en la base de datos."""
        cursor = self.cnx.cursor()
        cursor.execute('SELECT curso FROM Curso')
        alumnos = []
        for seccion in cursor:
            alumnos.append(str(seccion[0]))
        return alumnos

    def get_secciones5(self, codigo):
        """Obtener una lista de los nombres de los alumnos en la base de datos."""
        cursor = self.cnx.cursor()
        query = 'SELECT m.cod_alumno, n.1f, n.2f, n.3f FROM Nota AS n INNER JOIN Matricula AS m ON m.Cod_nota = n.codigo WHERE m.cod_clase = %s'
        cursor.execute(query, (codigo,))
        alumnos = [[alumno[0], alumno[1], alumno[2], alumno[3]] for alumno in cursor]
        return alumnos

    def get_secciones2(self, codigo):
        """Obtener una lista de los nombres de los alumnos en la base de datos."""
        cursor = self.cnx.cursor()
        cursor.execute('SELECT cod_nota FROM Matricula WHERE Seccion = %s', (codigo,))
        alumnos = []
        for alumno in cursor:
            alumnos.append(str(cod_nota[0]))
        return alumnos

    def get_secciones1(self, codigo, codigo0):
        """Obtener una lista de los nombres de los alumnos en la base de datos."""
        cursor = self.cnx.cursor()
        cursor.execute('SELECT Calificacion FROM Nota WHERE Alumno = %s and Seccion = %s', (codigo,codigo0))
        alumnos = []
        for calificacion in cursor:
            alumnos.append(str(calificacion[0]))
        return alumnos

    def get_secciones4(self, codigo):
        """Obtener una lista de los nombres de los alumnos en la base de datos."""
        cursor = self.cnx.cursor()
        cursor.execute('SELECT m.cod_alumno , n.1f, n.2f, n.3f FROM Nota AS n INNER JOIN Matricula AS m ON m.Cod_nota = n.codigo WHERE m.cod_clase= %s', (codigo,))
        data = cursor.fetchall()
        row_count = len(data)
        column_count = len(data[0])
        self.tableWidget.setRowCount(row_count)
        self.tableWidget.setColumnCount(column_count)
        for row in range(row_count):
            for column in range(column_count):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(data[row][column])))

    def get_secciones6(self, codigo):
        cursor = self.cnx.cursor()
        query = 'SELECT m.cod_alumno, n.1f, n.2f, n.3f FROM Nota AS n INNER JOIN Matricula AS m ON m.Cod_nota = n.codigo WHERE m.cod_clase = %s'
        cursor.execute(query, (codigo,))
        alumnos = [alumno for alumno in cursor]

        # Limpiar la tabla antes de agregar los datos
        self.table_list_widget.clearContents()

        # Agregar los datos a la tabla
        for i, alumno in enumerate(alumnos):
            data = [str(d) for d in alumno]
            for j, d in enumerate(data):
                item = QtWidgets.QTableWidgetItem(d)
                self.table_list_widget.setItem(i, j, item)

    def update_alumno_combo_box(self):
        # Actualizar el ComboBox de alumno en función del ComboBox de sección
        seccion_text = self.seccion_combo_box.currentText()
        codigos = seccion_text.split('(')[-1].strip(')').replace(',', '')
        self.alumno_combo_box.clear()
        self.get_secciones6(codigos)
        #self.alumno_combo_box.addItems(self.get_secciones0(codigos))
        # Ocultar el ComboBox de nota
        #self.nota_combo_box.show()

    def update_nota_combo_box(self):
        # Actualizar el ComboBox de nota en función del ComboBox de alumno
        alumno_text = self.alumno_combo_box.currentText()
        seccion_text = self.seccion_combo_box.currentText()
        codigo = alumno_text.split('(')[-1].strip(')').replace(',', '')  # Extraer el código del alumno de la selección
        codigo0=seccion_text.split('(')[-1].strip(')').replace(',', '')

        print(codigo)
        print("-.-")
        print(codigo0)

        self.table_list_widget.clear()
        self.table_list_widget.show()
        #self.table0_list_widget.clear()
        #self.table0_list_widget.show()
        #self.table1_list_widget.clear()
        #self.table1_list_widget.show()
        #self.table2_list_widget.clear()
        #self.table2_list_widget.show()
        secciones=[]
        secciones=self.get_secciones0(codigo0)
        secciones0=self.get_secciones1(codigo, codigo0)

        for i, seccion in enumerate(secciones):
            item0 = QTableWidgetItem(str(seccion))
            self.table_list_widget.setItem(i, 0, item0)
            print(item0.text())
            secciones0=self.get_secciones1(item0.text(), seccion)
            for j, seccion0 in enumerate(secciones0):
                item1 = QTableWidgetItem(str(seccion0))
                self.table_list_widget.setItem(i, j+1, item1)
                print(item1.text())    
if __name__ == '__main__':
    app = QApplication([])
    window = AuthenticationWindow()
    app.exec_()