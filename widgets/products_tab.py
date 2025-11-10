from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QTableWidget, 
                            QTableWidgetItem, QHeaderView, QGroupBox,
                            QMessageBox, QComboBox, QListWidget, QListWidgetItem,
                            QSpinBox, QDoubleSpinBox, QTabWidget)
from PyQt6.QtCore import Qt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db

class ProductsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.current_product_id = None
        self.current_ingredients = [] 
        self.current_semi_finished = []  
        self._setup_ui()
        self._load_products()
        self._load_ingredients()
        self._load_semi_finished()
    
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        title_label = QLabel("Управление продуктами")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title_label)
        
        content_layout = QHBoxLayout()
        
        left_panel = QWidget()
        left_panel.setMaximumWidth(500)
        left_layout = QVBoxLayout(left_panel)
        
        self._create_products_group(left_layout)
        
        self._create_composition_group(left_layout)
        
        content_layout.addWidget(left_panel)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        self._create_products_table(right_layout)
        
        content_layout.addWidget(right_panel, 1)
        
        main_layout.addLayout(content_layout)
    
    def _create_products_group(self, layout):
        group = QGroupBox("Управление продуктами")
        group_layout = QVBoxLayout(group)
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Название продукта")
        group_layout.addWidget(QLabel("Название:"))
        group_layout.addWidget(self.name_edit)
        
        buttons_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Добавить продукт")
        self.add_button.clicked.connect(self._on_add_product)
        buttons_layout.addWidget(self.add_button)
        
        self.update_button = QPushButton("Изменить продукт")
        self.update_button.clicked.connect(self._on_update_product)
        self.update_button.setEnabled(False)
        buttons_layout.addWidget(self.update_button)
        
        self.delete_button = QPushButton("Удалить продукт")
        self.delete_button.clicked.connect(self._on_delete_product)
        self.delete_button.setEnabled(False)
        self.delete_button.setStyleSheet("background-color: #ff6b6b; color: white;")
        buttons_layout.addWidget(self.delete_button)
        
        group_layout.addLayout(buttons_layout)
        
        layout.addWidget(group)
    
    def _create_composition_group(self, layout):
        group = QGroupBox("Состав продукта")
        group_layout = QVBoxLayout(group)
        
        self.composition_tabs = QTabWidget()
        
        ingredients_tab = QWidget()
        ingredients_layout = QVBoxLayout(ingredients_tab)
        
        ingredient_select_layout = QHBoxLayout()
        
        self.ingredient_combo = QComboBox()
        self.ingredient_combo.setPlaceholderText("Выберите ингридиент")
        ingredient_select_layout.addWidget(QLabel("Ингридиент:"))
        ingredient_select_layout.addWidget(self.ingredient_combo, 1)
        
        self.ingredient_quantity_spin = QDoubleSpinBox()
        self.ingredient_quantity_spin.setRange(1, 10000)
        self.ingredient_quantity_spin.setValue(100)
        self.ingredient_quantity_spin.setSuffix(" г")
        ingredient_select_layout.addWidget(QLabel("Количество:"))
        ingredient_select_layout.addWidget(self.ingredient_quantity_spin)
        
        ingredients_layout.addLayout(ingredient_select_layout)
        
        ingredient_buttons_layout = QHBoxLayout()
        
        self.add_ingredient_button = QPushButton("Добавить ингридиент")
        self.add_ingredient_button.clicked.connect(self._on_add_ingredient_to_list)
        ingredient_buttons_layout.addWidget(self.add_ingredient_button)
        
        self.remove_ingredient_button = QPushButton("Удалить ингридиент")
        self.remove_ingredient_button.clicked.connect(self._on_remove_ingredient_from_list)
        self.remove_ingredient_button.setEnabled(False)
        ingredient_buttons_layout.addWidget(self.remove_ingredient_button)
        
        ingredients_layout.addLayout(ingredient_buttons_layout)
        
        ingredients_layout.addWidget(QLabel("Ингридиенты в составе:"))
        self.ingredients_list = QListWidget()
        self.ingredients_list.itemSelectionChanged.connect(self._on_ingredient_selection_changed)
        ingredients_layout.addWidget(self.ingredients_list)
        
        self.composition_tabs.addTab(ingredients_tab, "Ингридиенты")
        
        semi_finished_tab = QWidget()
        semi_finished_layout = QVBoxLayout(semi_finished_tab)
        
        sf_select_layout = QHBoxLayout()
        
        self.semi_finished_combo = QComboBox()
        self.semi_finished_combo.setPlaceholderText("Выберите полуфабрикат")
        sf_select_layout.addWidget(QLabel("Полуфабрикат:"))
        sf_select_layout.addWidget(self.semi_finished_combo, 1)
        
        self.sf_quantity_spin = QDoubleSpinBox()
        self.sf_quantity_spin.setRange(1, 10000)
        self.sf_quantity_spin.setValue(100)
        self.sf_quantity_spin.setSuffix(" г")
        sf_select_layout.addWidget(QLabel("Количество:"))
        sf_select_layout.addWidget(self.sf_quantity_spin)
        
        semi_finished_layout.addLayout(sf_select_layout)
        
        sf_buttons_layout = QHBoxLayout()
        
        self.add_sf_button = QPushButton("Добавить полуфабрикат")
        self.add_sf_button.clicked.connect(self._on_add_semi_finished_to_list)
        sf_buttons_layout.addWidget(self.add_sf_button)
        
        self.remove_sf_button = QPushButton("Удалить полуфабрикат")
        self.remove_sf_button.clicked.connect(self._on_remove_semi_finished_from_list)
        self.remove_sf_button.setEnabled(False)
        sf_buttons_layout.addWidget(self.remove_sf_button)
        
        semi_finished_layout.addLayout(sf_buttons_layout)
        
        semi_finished_layout.addWidget(QLabel("Полуфабрикаты в составе:"))
        self.semi_finished_list = QListWidget()
        self.semi_finished_list.itemSelectionChanged.connect(self._on_semi_finished_selection_changed)
        semi_finished_layout.addWidget(self.semi_finished_list)
        
        self.composition_tabs.addTab(semi_finished_tab, "Полуфабрикаты")
        
        group_layout.addWidget(self.composition_tabs)
        
        composition_buttons_layout = QHBoxLayout()
        
        self.save_composition_button = QPushButton("Сохранить состав в БД")
        self.save_composition_button.clicked.connect(self._on_save_composition)
        self.save_composition_button.setEnabled(True)
        self.save_composition_button.setStyleSheet("background-color: #4CAF50; color: white;")
        composition_buttons_layout.addWidget(self.save_composition_button)
        
        self.load_composition_button = QPushButton("Загрузить состав из БД")
        self.load_composition_button.clicked.connect(self._on_load_composition)
        self.load_composition_button.setEnabled(False)
        self.load_composition_button.setStyleSheet("background-color: #2196F3; color: white;")
        composition_buttons_layout.addWidget(self.load_composition_button)
        
        group_layout.addLayout(composition_buttons_layout)
        
        self.nutrition_label = QLabel("Добавьте компоненты для расчета КБЖУ")
        self.nutrition_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin: 5px;")
        group_layout.addWidget(self.nutrition_label)
        
        layout.addWidget(group)
    
    def _create_products_table(self, layout):
        self.table_label = QLabel("Список продуктов:")
        self.table_label.setStyleSheet("font-weight: bold; margin: 5px;")
        layout.addWidget(self.table_label)
        
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(7)
        self.products_table.setHorizontalHeaderLabels([
            "ID", "Название", "Калории", "Белки", "Жиры", "Углеводы", "кДж"
        ])
        
        header = self.products_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Название растягивается
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Калории
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Белки
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Жиры
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Углеводы
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # кДж
        
        self.products_table.itemSelectionChanged.connect(self._on_table_selection_changed)
        layout.addWidget(self.products_table)
    
    def _load_products(self):
        """Загрузка продуктов из БД с расчетом КБЖУ"""
        try:
            products = db.get_all_products()
            self.products_table.setRowCount(len(products))
            
            for row, product in enumerate(products):
                nutrition = db.calculate_product_nutrition(product[0])
                
                self.products_table.setItem(row, 0, QTableWidgetItem(str(product[0])))  # ID
                self.products_table.setItem(row, 1, QTableWidgetItem(str(product[1])))  # Название
                self.products_table.setItem(row, 2, QTableWidgetItem(str(nutrition['calories'])))  # Калории
                self.products_table.setItem(row, 3, QTableWidgetItem(str(nutrition['proteins'])))  # Белки
                self.products_table.setItem(row, 4, QTableWidgetItem(str(nutrition['fats'])))  # Жиры
                self.products_table.setItem(row, 5, QTableWidgetItem(str(nutrition['carbs'])))  # Углеводы
                self.products_table.setItem(row, 6, QTableWidgetItem(str(nutrition['kJoule'])))  # кДж
            
            self.table_label.setText(f"Список продуктов (всего: {len(products)})")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить продукты: {str(e)}")
    
    def _load_ingredients(self):
        """Загрузка ингридиентов для комбобокса"""
        try:
            ingredients = db.get_all_ingredients()
            self.ingredient_combo.clear()
            
            for ingredient in ingredients:
                self.ingredient_combo.addItem(
                    f"{ingredient[1]} (К:{ingredient[2]} Б:{ingredient[4]} Ж:{ingredient[5]} У:{ingredient[6]})",
                    ingredient[0]
                )
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить ингридиенты: {str(e)}")
    
    def _load_semi_finished(self):
        """Загрузка полуфабрикатов для комбобокса"""
        try:
            semi_finished = db.get_all_semi_finished()
            self.semi_finished_combo.clear()
            
            for sf in semi_finished:
                nutrition = db.calculate_semi_finished_nutrition(sf[0])
                self.semi_finished_combo.addItem(
                    f"{sf[1]} (К:{nutrition['calories']} Б:{nutrition['proteins']} Ж:{nutrition['fats']} У:{nutrition['carbs']})",
                    sf[0]
                )
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить полуфабрикаты: {str(e)}")
    
    def _clear_composition(self):
        """Очистка состава"""
        self.current_ingredients.clear()
        self.current_semi_finished.clear()
        self.ingredients_list.clear()
        self.semi_finished_list.clear()
        self.nutrition_label.setText("Добавьте компоненты для расчета КБЖУ")
    
    
    def _calculate_and_display_nutrition(self):
        """Расчет и отображение пищевой ценности продукта"""
        if not self.current_ingredients and not self.current_semi_finished:
            self.nutrition_label.setText("Состав пустой")
            return
        
        total_weight = 0
        total_calories = 0
        total_kJoule = 0
        total_proteins = 0
        total_fats = 0
        total_carbs = 0
        
        for ingredient in self.current_ingredients:
            factor = ingredient['quantity'] / 100.0
            total_weight += ingredient['quantity']
            total_calories += ingredient['calories'] * factor
            total_kJoule += ingredient['calories'] * 4.184 * factor
            total_proteins += ingredient['proteins'] * factor
            total_fats += ingredient['fats'] * factor
            total_carbs += ingredient['carbs'] * factor
        
        for sf in self.current_semi_finished:
            sf_nutrition = db.calculate_semi_finished_nutrition(sf['id'])
            factor = sf['quantity'] / 100.0
            total_weight += sf['quantity']
            total_calories += sf_nutrition['calories'] * factor
            total_kJoule += sf_nutrition['kJoule'] * factor
            total_proteins += sf_nutrition['proteins'] * factor
            total_fats += sf_nutrition['fats'] * factor
            total_carbs += sf_nutrition['carbs'] * factor
        
        if total_weight == 0:
            self.nutrition_label.setText("Ошибка: нулевой вес")
            return
        
        factor_to_100g = 100.0 / total_weight
        
        nutrition = {
            'calories': round(total_calories * factor_to_100g, 2),
            'kJoule': round(total_kJoule * factor_to_100g, 2),
            'proteins': round(total_proteins * factor_to_100g, 2),
            'fats': round(total_fats * factor_to_100g, 2),
            'carbs': round(total_carbs * factor_to_100g, 2)
        }
        
        self.nutrition_label.setText(
            f"КБЖУ на 100г: К:{nutrition['calories']} "
            f"Б:{nutrition['proteins']} Ж:{nutrition['fats']} У:{nutrition['carbs']}"
        )


    def _on_table_selection_changed(self):
        """Обработчик выбора продукта в таблице"""
        selected_items = self.products_table.selectedItems()
        if not selected_items:
            self.current_product_id = None
            self.update_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.load_composition_button.setEnabled(False)
            self.name_edit.clear()
            self._clear_composition()
            return
        
        row = selected_items[0].row()
        self.current_product_id = int(self.products_table.item(row, 0).text())
        name = self.products_table.item(row, 1).text()
        
        self.name_edit.setText(name)
        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)
        self.load_composition_button.setEnabled(True)
        
        self._load_composition_from_db(self.current_product_id)
    
    def _on_ingredient_selection_changed(self):
        """Обработчик выбора ингридиента в списке"""
        self.remove_ingredient_button.setEnabled(len(self.ingredients_list.selectedItems()) > 0)
    
    def _on_semi_finished_selection_changed(self):
        """Обработчик выбора полуфабриката в списке"""
        self.remove_sf_button.setEnabled(len(self.semi_finished_list.selectedItems()) > 0)
    
    def _on_add_product(self):
        """Обработчик добавления продукта"""
        name = self.name_edit.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название продукта")
            return
        
        if db.product_exists(name):
            QMessageBox.warning(self, "Ошибка", "Продукт с таким названием уже существует")
            return
        
        if not self.current_ingredients and not self.current_semi_finished:
            reply = QMessageBox.question(
                self,
                "Пустой состав",
                "Вы создаете продукт без компонентов. Продолжить?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        try:
            product_id = db.add_product(name)
            print(f"создание продукта name:{name} id:{product_id}")
            
            self._save_composition_to_db(product_id)
            
            self.name_edit.clear()
            self._clear_composition()
            self._load_products()
            
            QMessageBox.information(self, "Успех", f"Продукт '{name}' добавлен!")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить продукт: {str(e)}")
    
    def _on_update_product(self):
        """Обработчик обновления продукта"""
        if not self.current_product_id:
            return
        
        name = self.name_edit.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название продукта")
            return
        
        if db.product_exists(name, self.current_product_id):
            QMessageBox.warning(self, "Ошибка", "Продукт с таким названием уже существует")
            return
        
        try:
            success = db.update_product(self.current_product_id, name)
            
            if success:
                print(f"обновление продукта id:{self.current_product_id} name:{name}")
                self._load_products()
                QMessageBox.information(self, "Успех", "Название продукта обновлено!")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось обновить продукт")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось обновить продукт: {str(e)}")
    
    def _on_delete_product(self):
        """Обработчик удаления продукта"""
        if not self.current_product_id:
            return
        
        try:
            product = db.get_product(self.current_product_id)
            if not product:
                QMessageBox.warning(self, "Ошибка", "Продукт не найден")
                return
            
            reply = QMessageBox.question(
                self, 
                "Подтверждение удаления", 
                f"Вы уверены, что хотите удалить продукт '{product['name']}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                success = db.delete_product(self.current_product_id)
                
                if success:
                    print(f"удаление продукта id:{self.current_product_id}")
                    self.current_product_id = None
                    self.name_edit.clear()
                    self.update_button.setEnabled(False)
                    self.delete_button.setEnabled(False)
                    self.load_composition_button.setEnabled(False)
                    self._clear_composition()
                    self._load_products()
                    QMessageBox.information(self, "Успех", "Продукт удален!")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить продукт")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить продукт: {str(e)}")
    
    def _on_add_ingredient_to_list(self):
        """Обработчик добавления ингридиента в локальный список"""
        if self.ingredient_combo.currentIndex() == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите ингридиент")
            return
        
        ingredient_id = self.ingredient_combo.currentData()
        ingredient_name = self.ingredient_combo.currentText().split(' (')[0]
        quantity = self.ingredient_quantity_spin.value()
        
        for ingredient in self.current_ingredients:
            if ingredient['id'] == ingredient_id:
                QMessageBox.warning(self, "Ошибка", "Этот ингридиент уже добавлен в состав")
                return
        
        try:
            ingredient_data = db.get_ingredient(ingredient_id)
            if not ingredient_data:
                QMessageBox.warning(self, "Ошибка", "Ингридиент не найден в базе")
                return
            
            new_ingredient = {
                'id': ingredient_id,
                'name': ingredient_name,
                'quantity': quantity,
                'calories': ingredient_data['calories'],
                'proteins': ingredient_data['proteins'],
                'fats': ingredient_data['fats'],
                'carbs': ingredient_data['carbs']
            }
            self.current_ingredients.append(new_ingredient)
            
            item = QListWidgetItem(
                f"{ingredient_name} - {quantity}г "
                f"(К:{ingredient_data['calories']} Б:{ingredient_data['proteins']} "
                f"Ж:{ingredient_data['fats']} У:{ingredient_data['carbs']})"
            )
            item.setData(Qt.ItemDataRole.UserRole, ingredient_id)
            self.ingredients_list.addItem(item)
            
            print(f"добавление ингридиента в список: {ingredient_name} - {quantity}г")
            
            self._calculate_and_display_nutrition()
            
            self.ingredient_quantity_spin.setValue(100)
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить ингридиент: {str(e)}")
    
    def _on_remove_ingredient_from_list(self):
        """Обработчик удаления ингридиента из локального списка"""
        selected_items = self.ingredients_list.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        ingredient_id = item.data(Qt.ItemDataRole.UserRole)
        ingredient_name = item.text().split(' - ')[0]
        
        self.current_ingredients = [ing for ing in self.current_ingredients if ing['id'] != ingredient_id]
        
        self.ingredients_list.takeItem(self.ingredients_list.row(item))
        
        print(f"удаление ингридиента из списка: {ingredient_name}")
        
        self._calculate_and_display_nutrition()
    
    def _on_add_semi_finished_to_list(self):
        """Обработчик добавления полуфабриката в локальный список"""
        if self.semi_finished_combo.currentIndex() == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите полуфабрикат")
            return
        
        sf_id = self.semi_finished_combo.currentData()
        sf_name = self.semi_finished_combo.currentText().split(' (')[0]
        quantity = self.sf_quantity_spin.value()
        
        for sf in self.current_semi_finished:
            if sf['id'] == sf_id:
                QMessageBox.warning(self, "Ошибка", "Этот полуфабрикат уже добавлен в состав")
                return
        
        try:
            sf_data = db.get_semi_finished(sf_id)
            if not sf_data:
                QMessageBox.warning(self, "Ошибка", "Полуфабрикат не найден в базе")
                return
            
            new_sf = {
                'id': sf_id,
                'name': sf_name,
                'quantity': quantity
            }
            self.current_semi_finished.append(new_sf)
            
            nutrition = db.calculate_semi_finished_nutrition(sf_id)
            
            item = QListWidgetItem(
                f"{sf_name} - {quantity}г "
                f"(К:{nutrition['calories']} Б:{nutrition['proteins']} "
                f"Ж:{nutrition['fats']} У:{nutrition['carbs']})"
            )
            item.setData(Qt.ItemDataRole.UserRole, sf_id)
            self.semi_finished_list.addItem(item)
            
            print(f"добавление полуфабриката в список: {sf_name} - {quantity}г")
            
            self._calculate_and_display_nutrition()
            
            self.sf_quantity_spin.setValue(100)
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить полуфабрикат: {str(e)}")
    
    def _on_remove_semi_finished_from_list(self):
        """Обработчик удаления полуфабриката из локального списка"""
        selected_items = self.semi_finished_list.selectedItems()
        if not selected_items:
            return
        
        item = selected_items[0]
        sf_id = item.data(Qt.ItemDataRole.UserRole)
        sf_name = item.text().split(' - ')[0]
        
        self.current_semi_finished = [sf for sf in self.current_semi_finished if sf['id'] != sf_id]
        
        self.semi_finished_list.takeItem(self.semi_finished_list.row(item))
        
        print(f"удаление полуфабриката из списка: {sf_name}")
        
        self._calculate_and_display_nutrition()
    
    def _save_composition_to_db(self, product_id):
        """Сохранение состава в БД"""
        for ingredient in self.current_ingredients:
            success = db.add_ingredient_to_product(
                product_id,
                ingredient['id'],
                ingredient['quantity']
            )
            if not success:
                raise Exception(f"Не удалось добавить ингридиент {ingredient['name']}")
        
        for sf in self.current_semi_finished:
            success = db.add_semi_finished_to_product(
                product_id,
                sf['id'],
                sf['quantity']
            )
            if not success:
                raise Exception(f"Не удалось добавить полуфабрикат {sf['name']}")
    
    def _load_composition_from_db(self, product_id):
        """Загрузка состава продукта из БД в локальный список"""
        try:
            self.current_ingredients.clear()
            self.current_semi_finished.clear()
            self.ingredients_list.clear()
            self.semi_finished_list.clear()
            
            ingredients = db.get_product_ingredients(product_id)
            for ingredient in ingredients:
                ingredient_data = {
                    'id': ingredient['id'],
                    'name': ingredient['name'],
                    'quantity': ingredient['quantity'],
                    'calories': ingredient['calories'],
                    'proteins': ingredient['proteins'],
                    'fats': ingredient['fats'],
                    'carbs': ingredient['carbs']
                }
                self.current_ingredients.append(ingredient_data)
                
                item = QListWidgetItem(
                    f"{ingredient['name']} - {ingredient['quantity']}г "
                    f"(К:{ingredient['calories']} Б:{ingredient['proteins']} "
                    f"Ж:{ingredient['fats']} У:{ingredient['carbs']})"
                )
                item.setData(Qt.ItemDataRole.UserRole, ingredient['id'])
                self.ingredients_list.addItem(item)
            
            semi_finished = db.get_product_semi_finished(product_id)
            for sf in semi_finished:
                sf_data = {
                    'id': sf['id'],
                    'name': sf['name'],
                    'quantity': sf['quantity']
                }
                self.current_semi_finished.append(sf_data)
                
                nutrition = db.calculate_semi_finished_nutrition(sf['id'])
                
                item = QListWidgetItem(
                    f"{sf['name']} - {sf['quantity']}г "
                    f"(К:{nutrition['calories']} Б:{nutrition['proteins']} "
                    f"Ж:{nutrition['fats']} У:{nutrition['carbs']})"
                )
                item.setData(Qt.ItemDataRole.UserRole, sf['id'])
                self.semi_finished_list.addItem(item)
            
            self._calculate_and_display_nutrition()
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить состав: {str(e)}")
    
    def _on_save_composition(self):
        """Обработчик сохранения состава в БД"""
        if not self.current_product_id:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите или создайте продукт")
            return
        
        if not self.current_ingredients and not self.current_semi_finished:
            QMessageBox.warning(self, "Ошибка", "Нельзя сохранить пустой состав")
            return
        
        try:
            old_ingredients = db.get_product_ingredients(self.current_product_id)
            for old_ing in old_ingredients:
                db.remove_ingredient_from_product(self.current_product_id, old_ing['id'])
            
            old_semi_finished = db.get_product_semi_finished(self.current_product_id)
            for old_sf in old_semi_finished:
                db.remove_semi_finished_from_product(self.current_product_id, old_sf['id'])
            
            self._save_composition_to_db(self.current_product_id)
            
            print(f"сохранение состава для продукта id:{self.current_product_id}")
        
            self._load_products()
            
            QMessageBox.information(self, "Успех", "Состав продукта сохранен в БД!")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить состав: {str(e)}")
    
    def _on_load_composition(self):
        """Обработчик загрузки состава из БД"""
        if not self.current_product_id:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите продукт")
            return
        
        try:
            self._load_composition_from_db(self.current_product_id)
            QMessageBox.information(self, "Успех", "Состав загружен из БД!")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить состав: {str(e)}")