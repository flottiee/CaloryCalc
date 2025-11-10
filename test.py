import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tab_widget = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_widget.setGeometry(QtCore.QRect(0, 0, 800, 500))
        
        # Вкладка "Калькулятор"
        self.calculator_tab = QWidget()
        self.tab_widget.addTab(self.calculator_tab, "Calculator")
        # Вкладка "Ингредиенты"
        self.ingredients_tab = QWidget()
        self.init_ingredients_tab()
        self.tab_widget.addTab(self.ingredients_tab, "Ingredients")
        # Вкладка "Полуфабрикаты"
        self.semi_finished_tab = QWidget()
        self.init_semi_finished_tab()
        self.tab_widget.addTab(self.semi_finished_tab, "Semi-finished")
        # Вкладка "Продукция"
        self.products_tab = QWidget()
        self.tab_widget.addTab(self.products_tab, "Products")
        MainWindow.setCentralWidget(self.centralwidget)
    def init_ingredients_tab(self):
        layout = QtWidgets.QVBoxLayout()
        # Заголовок
        layout.addWidget(QtWidgets.QLabel("Ingredients Management"))
        # Таблица для ингредиентов
        self.ingredients_table = QtWidgets.QTableWidget()
        self.ingredients_table.setColumnCount(5)
        self.ingredients_table.setHorizontalHeaderLabels(["ID", "Name", "Calories", "Proteins", "Fats", "Carbs"])
        layout.addWidget(self.ingredients_table)
        #------------------------------------------------------------
        # Поля для добавления ингредиентов
        self.name_input = QtWidgets.QLineEdit()
        self.calories_input = QtWidgets.QLineEdit()
        self.proteins_input = QtWidgets.QLineEdit()
        self.fats_input = QtWidgets.QLineEdit()
        self.carbs_input = QtWidgets.QLineEdit()
        #Раздел для добавления ингридиента в таблицу
        layout.addWidget(QtWidgets.QLabel("Add Ingredient"))
        layout.addWidget(QtWidgets.QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QtWidgets.QLabel("Calories:"))
        layout.addWidget(self.calories_input)
        layout.addWidget(QtWidgets.QLabel("Proteins:"))
        layout.addWidget(self.proteins_input)
        layout.addWidget(QtWidgets.QLabel("Fats:"))
        layout.addWidget(self.fats_input)
        layout.addWidget(QtWidgets.QLabel("Carbs:"))
        layout.addWidget(self.carbs_input)
        add_button = QtWidgets.QPushButton("Add Ingredient")
        #------------------------------------------------------------
        # Поля для изменения ингредиента
        self.id_update_input = QtWidgets.QLineEdit()
        self.name_update_input = QtWidgets.QLineEdit()
        self.calories_update_input = QtWidgets.QLineEdit()
        self.proteins_update_input = QtWidgets.QLineEdit()
        self.fats_update_input = QtWidgets.QLineEdit()
        self.carbs_update_input = QtWidgets.QLineEdit()
        #Раздел для изменения ингридиента в таблице
        layout.addWidget(QtWidgets.QLabel("Изменить Ingredient"))
        layout.addWidget(QtWidgets.QLabel("Id:"))
        layout.addWidget(self.name_update_input)
        layout.addWidget(QtWidgets.QLabel("Name:"))
        layout.addWidget(self.name_update_input)
        layout.addWidget(QtWidgets.QLabel("Calories:"))
        layout.addWidget(self.calories_update_input)
        layout.addWidget(QtWidgets.QLabel("Proteins:"))
        layout.addWidget(self.proteins_update_input)
        layout.addWidget(QtWidgets.QLabel("Fats:"))
        layout.addWidget(self.fats_update_input)
        layout.addWidget(QtWidgets.QLabel("Carbs:"))
        layout.addWidget(self.carbs_update_input)
        add_button = QtWidgets.QPushButton("Update Ingredient")
        # Кнопки для действий
        buttons_layout = QtWidgets.QHBoxLayout()
        update_button = QtWidgets.QPushButton("Update Ingredient")
        delete_button = QtWidgets.QPushButton("Delete Ingredient")
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(update_button)
        buttons_layout.addWidget(delete_button)
        layout.addLayout(buttons_layout)
        # Подключение кнопок к функциям
        add_button.clicked.connect(self.add_ingredient)
        update_button.clicked.connect(self.update_ingredient)
        delete_button.clicked.connect(self.delete_ingredient)
        self.ingredients_tab.setLayout(layout)
    def add_ingredient(self):
        name = self.name_input.text().strip()
        calories = self.calories_input.text().strip()
        proteins = self.proteins_input.text().strip()
        fats = self.fats_input.text().strip()
        carbs = self.carbs_input.text().strip()
        # Здесь должен быть код для добавления ингредиента в БД.
        print(f"Adding ingredient: {name}, C: {calories}, P: {proteins}, F: {fats}, C: {carbs}")
        self.clear_ingredient_inputs()
    def update_ingredient(self):
        selected_row = self.ingredients_table.currentRow()
        if selected_row >= 0:
            ingredient_id = self.ingredients_table.item(selected_row, 0).text()
            name = self.name_input.text().strip()
            calories = self.calories_input.text().strip()
            proteins = self.proteins_input.text().strip()
            fats = self.fats_input.text().strip()
            carbs = self.carbs_input.text().strip()
            # Здесь должен быть код для обновления ингредиента в БД.
            print(f"Updating ingredient ID {ingredient_id} to {name}, C: {calories}, P: {proteins}, F: {fats}, C: {carbs}")
            self.clear_ingredient_inputs()
    def delete_ingredient(self):
        selected_row = self.ingredients_table.currentRow()
        if selected_row >= 0:
            ingredient_id = self.ingredients_table.item(selected_row, 0).text()
            # Здесь должен быть код для удаления ингредиента из БД.
            print(f"Deleting ingredient ID {ingredient_id}")
            self.ingredients_table.removeRow(selected_row)
    def clear_ingredient_inputs(self):
        self.name_input.clear()
        self.calories_input.clear()
        self.proteins_input.clear()
        self.fats_input.clear()
        self.carbs_input.clear()
    def init_semi_finished_tab(self):
        layout = QtWidgets.QVBoxLayout()
        # Заголовок
        layout.addWidget(QtWidgets.QLabel("Semi-finished Products Management"))
        # Таблица для полуфабрикатов
        self.semi_finished_table = QtWidgets.QTableWidget()
        self.semi_finished_table.setColumnCount(4)  # ID, Name, Calories, Proteins, Fats, Carbs
        self.semi_finished_table.setHorizontalHeaderLabels(["ID", "Name", "Ingredients", "Total Nutrition"])
        layout.addWidget(self.semi_finished_table)
        # Поля для добавления полуфабрикатов
        self.semi_finished_name_input = QtWidgets.QLineEdit()
        layout.addWidget(QtWidgets.QLabel("Add Semi-finished Product:"))
        layout.addWidget(QtWidgets.QLabel("Name:"))
        layout.addWidget(self.semi_finished_name_input)
        # Кнопка для добавления полуфабриката
        add_semi_finished_button = QtWidgets.QPushButton("Add Semi-finished")
        layout.addWidget(add_semi_finished_button)
        add_semi_finished_button.clicked.connect(self.add_semi_finished)
        layout.addWidget(self.semi_finished_table)
        self.semi_finished_tab.setLayout(layout)
    def add_semi_finished(self):
        name = self.semi_finished_name_input.text()
        # Здесь должен быть код для добавления полуфабриката в БД.
        print(f"Adding semi-finished product: {name}")
        self.clear_semi_finished_inputs()
    def clear_semi_finished_inputs(self):
        self.semi_finished_name_input.clear()
def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()
