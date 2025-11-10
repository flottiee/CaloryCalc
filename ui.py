import sys
from PyQt6.QtWidgets import (
    QApplication, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox
)
class IngredientApp(QTabWidget):
    def _init_(self):
        super()._init_()
        self.init_ui()
    def init_ui(self):
        # Вкладка "Список ингредиентов"
        self.ingredients_tab = QWidget()
        self.init_ingredients_tab()
        self.addTab(self.ingredients_tab, "Ingredients")
        # Вкладка "Полуфабрикаты"
        self.semi_finished_tab = QWidget()
        self.init_semi_finished_tab()
        self.addTab(self.semi_finished_tab, "Semi-finished")
        # Пустая вкладка
        self.addTab(QWidget(), "Empty")
        self.setWindowTitle("Ingredient and Semi-finished Manager")
        self.resize(800, 600)
        self.show()
    def init_ingredients_tab(self):
        layout = QVBoxLayout()
        # Таблица для ингредиентов
        self.ingredients_table = QTableWidget()
        self.ingredients_table.setColumnCount(5)
        self.ingredients_table.setHorizontalHeaderLabels(["ID", "Name", "Calories", "Proteins", "Fats", "Carbs"])
        layout.addWidget(self.ingredients_table)
        # Поля для добавления/обновления ингредиентов
        form_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.calories_input = QLineEdit()
        self.proteins_input = QLineEdit()
        self.fats_input = QLineEdit()
        self.carbs_input = QLineEdit()
        
        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("Calories:"))
        form_layout.addWidget(self.calories_input)
        form_layout.addWidget(QLabel("Proteins:"))
        form_layout.addWidget(self.proteins_input)
        form_layout.addWidget(QLabel("Fats:"))
        form_layout.addWidget(self.fats_input)
        form_layout.addWidget(QLabel("Carbs:"))
        form_layout.addWidget(self.carbs_input)
        
        layout.addLayout(form_layout)
        # Кнопки для действий
        buttons_layout = QHBoxLayout()
        add_button = QPushButton("Add Ingredient")
        update_button = QPushButton("Update Ingredient")
        delete_button = QPushButton("Delete Ingredient")
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(update_button)
        buttons_layout.addWidget(delete_button)
        layout.addLayout(buttons_layout)
        self.ingredients_table.setRowCount(0)
        # Подключение кнопок к действиям
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
        if not name or not calories.isnumeric() or not proteins or not fats or not carbs:
            QMessageBox.warning(self, "Input Error", "Please enter valid data.")
            return
        # Здесь вы можете добавить код для вставки в БД
        # Например:
        # self.db.create_ingredient(name, int(calories), float(proteins), float(fats), float(carbs))
        
        print(f"Добавление ингредиента: {name}, Калории: {calories}, Белки: {proteins}, Жиры: {fats}, Углеводы: {carbs}")
        self.populate_ingredients_table()  # Обновить таблицу
        self.clear_inputs()
    def update_ingredient(self):
        selected_row = self.ingredients_table.currentRow()
        if selected_row >= 0:
            ingredient_id = self.ingredients_table.item(selected_row, 0).text()
            name = self.name_input.text().strip()
            calories = self.calories_input.text().strip()
            proteins = self.proteins_input.text().strip()
            fats = self.fats_input.text().strip()
            carbs = self.carbs_input.text().strip()
            if not name or not calories.isnumeric() or not proteins or not fats or not carbs:
                QMessageBox.warning(self, "Input Error", "Please enter valid data.")
                return
            # Здесь вы можете добавить код для обновления в БД
            # Например:
            # self.db.update_ingredient(ingredient_id, name, int(calories), float(proteins), float(fats), float(carbs))
            
            print(f"Изменение значения {name} в таблице ingredients с индексом {ingredient_id}")
            self.populate_ingredients_table()  # Обновить таблицу
            self.clear_inputs()
    def delete_ingredient(self):
        selected_row = self.ingredients_table.currentRow()
        if selected_row >= 0:
            ingredient_id = self.ingredients_table.item(selected_row, 0).text()
            # Здесь вы можете добавить код для удаления из БД
            # Например:
            # self.db.delete_ingredient(ingredient_id)
            print(f"Удаление ингредиента с индексом {ingredient_id}")
            self.ingredients_table.removeRow(selected_row)
    def clear_inputs(self):
        self.name_input.clear()
        self.calories_input.clear()
        self.proteins_input.clear()
        self.fats_input.clear()
        self.carbs_input.clear()
    def init_semi_finished_tab(self):
        layout = QVBoxLayout()
        # Таблица для полуфабрикатов
        self.semi_finished_table = QTableWidget()
        self.semi_finished_table.setColumnCount(2)
        self.semi_finished_table.setHorizontalHeaderLabels(["ID", "Name"])
        layout.addWidget(self.semi_finished_table)
        # Поля для добавления полуфабрикатов
        self.semi_finished_name_input = QLineEdit()
        layout.addWidget(QLabel("Semi-finished Name:"))
        layout.addWidget(self.semi_finished_name_input)
        # Кнопка для добавления полуфабриката
        add_semi_finished_button = QPushButton("Add Semi-finished")
        layout.addWidget(add_semi_finished_button)
        add_semi_finished_button.clicked.connect(self.add_semi_finished)
        layout.addWidget(self.semi_finished_table)
        self.semi_finished_tab.setLayout(layout)
    def add_semi_finished(self):
        name = self.semi_finished_name_input.text()
        # Здесь можно добавить код для добавления полуфабриката в БД
        # Например:
        # self.db.create_semi_finished(name)
        print(f"Добавление полуфабриката: {name}")
        self.populate_semi_finished_table()  # Мы обновляем таблицу
        self.semi_finished_name_input.clear()
    def populate_ingredients_table(self):
        """Заполняет таблицу ингредиентов. Здесь разместите код для получения данных из БД."""
        self.ingredients_table.setRowCount(0)
        # Например, получить данные из БД: ingredients = self.db.get_all_ingredients()
        ingredients = []  # Замените это пустым списком на выборку из БД
        for ingredient in ingredients:
            row_position = self.ingredients_table.rowCount()
            self.ingredients_table.insertRow(row_position)
            for column, data in enumerate(ingredient):
                self.ingredients_table.setItem(row_position, column, QTableWidgetItem(str(data)))
    def populate_semi_finished_table(self):
        """Заполняет таблицу полуфабрикатов. Здесь разместите код для получения данных из БД."""
        self.semi_finished_table.setRowCount(0)
        # Например, получить данные из БД: semi_finished = self.db.get_all_semi_finished()
        semi_finished = []  # Замените это пустым списком на выборку из БД
        for sf in semi_finished:
            row_position = self.semi_finished_table.rowCount()
            self.semi_finished_table.insertRow(row_position)
            self.semi_finished_table.setItem(row_position, 0, QTableWidgetItem(str(sf[0])))
            self.semi_finished_table.setItem(row_position, 1, QTableWidgetItem(sf[1]))

