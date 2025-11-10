from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QTableWidget, 
                            QTableWidgetItem, QHeaderView, QGroupBox,
                            QMessageBox, QComboBox, QListWidget, QListWidgetItem,
                            QSpinBox, QDoubleSpinBox)
from PyQt6.QtCore import Qt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db

class SemiFinishedTab(QWidget):
    def __init__(self):
        super().__init__()
        self.current_semi_finished_id = None
        self.current_ingredients = []  # Локальный список ингридиентов перед сохранением в БД
        self._setup_ui()
        self._load_semi_finished()
        self._load_ingredients()
    
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Заголовок
        title_label = QLabel("Управление полуфабрикатами")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # Область с формами (слева) и таблицей (справа)
        content_layout = QHBoxLayout()
        
        # Левая панель с формами
        left_panel = QWidget()
        left_panel.setMaximumWidth(500)
        left_layout = QVBoxLayout(left_panel)
        
        # Группа для управления полуфабрикатами
        self._create_semi_finished_group(left_layout)
        
        # Группа для управления ингридиентами полуфабриката
        self._create_ingredients_group(left_layout)
        
        content_layout.addWidget(left_panel)
        
        # Правая панель с таблицей
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Таблица полуфабрикатов
        self._create_semi_finished_table(right_layout)
        
        content_layout.addWidget(right_panel, 1)
        
        main_layout.addLayout(content_layout)
    
    def _create_semi_finished_group(self, layout):
        group = QGroupBox("Управление полуфабрикатами")
        group_layout = QVBoxLayout(group)
        
        # Поле для названия
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Название полуфабриката")
        group_layout.addWidget(QLabel("Название:"))
        group_layout.addWidget(self.name_edit)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Добавить ПФ")
        self.add_button.clicked.connect(self._on_add_semi_finished)
        buttons_layout.addWidget(self.add_button)
        
        self.update_button = QPushButton("Изменить ПФ")
        self.update_button.clicked.connect(self._on_update_semi_finished)
        self.update_button.setEnabled(False)
        buttons_layout.addWidget(self.update_button)
        
        self.delete_button = QPushButton("Удалить ПФ")
        self.delete_button.clicked.connect(self._on_delete_semi_finished)
        self.delete_button.setEnabled(False)
        self.delete_button.setStyleSheet("background-color: #ff6b6b; color: white;")
        buttons_layout.addWidget(self.delete_button)
        
        group_layout.addLayout(buttons_layout)
        
        layout.addWidget(group)
    
    def _create_ingredients_group(self, layout):
        group = QGroupBox("Ингридиенты полуфабриката")
        group_layout = QVBoxLayout(group)
        
        # Выбор ингридиента
        ingredients_layout = QHBoxLayout()
        
        self.ingredient_combo = QComboBox()
        self.ingredient_combo.setPlaceholderText("Выберите ингридиент")
        ingredients_layout.addWidget(QLabel("Ингридиент:"))
        ingredients_layout.addWidget(self.ingredient_combo, 1)
        
        self.quantity_spin = QDoubleSpinBox()
        self.quantity_spin.setRange(1, 10000)
        self.quantity_spin.setValue(100)
        self.quantity_spin.setSuffix(" г")
        ingredients_layout.addWidget(QLabel("Количество:"))
        ingredients_layout.addWidget(self.quantity_spin)
        
        group_layout.addLayout(ingredients_layout)
        
        # Кнопки для ингридиентов
        ingredient_buttons_layout = QHBoxLayout()
        
        self.add_ingredient_button = QPushButton("Добавить в список")
        self.add_ingredient_button.clicked.connect(self._on_add_ingredient_to_list)
        self.add_ingredient_button.setEnabled(True)  # Всегда активна для нового ПФ
        ingredient_buttons_layout.addWidget(self.add_ingredient_button)
        
        self.remove_ingredient_button = QPushButton("Удалить из списка")
        self.remove_ingredient_button.clicked.connect(self._on_remove_ingredient_from_list)
        self.remove_ingredient_button.setEnabled(False)
        ingredient_buttons_layout.addWidget(self.remove_ingredient_button)
        
        group_layout.addLayout(ingredient_buttons_layout)
        
        # Кнопка сохранения состава в БД
        self.save_composition_button = QPushButton("Сохранить состав в БД")
        self.save_composition_button.clicked.connect(self._on_save_composition)
        self.save_composition_button.setEnabled(True)
        self.save_composition_button.setStyleSheet("background-color: #4CAF50; color: white;")
        group_layout.addWidget(self.save_composition_button)
        
        # Кнопка загрузки состава из БД
        self.load_composition_button = QPushButton("Загрузить состав из БД")
        self.load_composition_button.clicked.connect(self._on_load_composition)
        self.load_composition_button.setEnabled(False)
        self.load_composition_button.setStyleSheet("background-color: #2196F3; color: white;")
        group_layout.addWidget(self.load_composition_button)
        
        # Список ингридиентов полуфабриката
        group_layout.addWidget(QLabel("Состав:"))
        self.ingredients_list = QListWidget()
        self.ingredients_list.itemSelectionChanged.connect(self._on_ingredient_selection_changed)
        group_layout.addWidget(self.ingredients_list)
        
        # Информация о пищевой ценности
        self.nutrition_label = QLabel("Добавьте ингридиенты для расчета КБЖУ")
        self.nutrition_label.setStyleSheet("font-weight: bold; color: #2c3e50; margin: 5px;")
        group_layout.addWidget(self.nutrition_label)
        
        layout.addWidget(group)
    
    def _create_semi_finished_table(self, layout):
        self.table_label = QLabel("Список полуфабрикатов:")
        self.table_label.setStyleSheet("font-weight: bold; margin: 5px;")
        layout.addWidget(self.table_label)
        
        self.semi_finished_table = QTableWidget()
        self.semi_finished_table.setColumnCount(2)
        self.semi_finished_table.setHorizontalHeaderLabels(["ID", "Название"])
        
        # Настройка таблицы
        header = self.semi_finished_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        self.semi_finished_table.itemSelectionChanged.connect(self._on_table_selection_changed)
        layout.addWidget(self.semi_finished_table)
    
    def _load_semi_finished(self):
        """Загрузка полуфабрикатов из БД"""
        try:
            semi_finished = db.get_all_semi_finished()
            self.semi_finished_table.setRowCount(len(semi_finished))
            
            for row, sf in enumerate(semi_finished):
                self.semi_finished_table.setItem(row, 0, QTableWidgetItem(str(sf[0])))  # ID
                self.semi_finished_table.setItem(row, 1, QTableWidgetItem(str(sf[1])))  # Название
            
            self.table_label.setText(f"Список полуфабрикатов (всего: {len(semi_finished)})")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить полуфабрикаты: {str(e)}")
    
    def _load_ingredients(self):
        """Загрузка ингридиентов для комбобокса"""
        try:
            ingredients = db.get_all_ingredients()
            self.ingredient_combo.clear()
            
            for ingredient in ingredients:
                self.ingredient_combo.addItem(
                    f"{ingredient[1]} (К:{ingredient[2]} Б:{ingredient[4]} Ж:{ingredient[5]} У:{ingredient[6]})",
                    ingredient[0]  # ID как userData
                )
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить ингридиенты: {str(e)}")
    
    def _clear_composition(self):
        """Очистка состава"""
        self.current_ingredients.clear()
        self.ingredients_list.clear()
        self.nutrition_label.setText("Добавьте ингридиенты для расчета КБЖУ")
    
    def _load_composition_from_db(self, semi_finished_id):
        """Загрузка состава полуфабриката из БД в локальный список"""
        try:
            ingredients = db.get_semi_finished_ingredients(semi_finished_id)
            self.current_ingredients.clear()
            self.ingredients_list.clear()
            
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
            
            # Расчет и отображение КБЖУ
            self._calculate_and_display_nutrition()
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить состав: {str(e)}")
    
    def _calculate_and_display_nutrition(self):
        """Расчет и отображение пищевой ценности"""
        if not self.current_ingredients:
            self.nutrition_label.setText("Состав пустой")
            return
        
        total_weight = sum(ingredient['quantity'] for ingredient in self.current_ingredients)
        
        if total_weight == 0:
            self.nutrition_label.setText("Ошибка: нулевой вес")
            return
        
        # Рассчитываем суммарные значения
        total_calories = 0
        total_kJoule = 0
        total_proteins = 0
        total_fats = 0
        total_carbs = 0
        
        for ingredient in self.current_ingredients:
            factor = ingredient['quantity'] / 100.0
            total_calories += ingredient['calories'] * factor
            total_kJoule += ingredient['calories'] * 4.184 * factor  # Расчет kJoule
            total_proteins += ingredient['proteins'] * factor
            total_fats += ingredient['fats'] * factor
            total_carbs += ingredient['carbs'] * factor
        
        # Приводим к 100г
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
        """Обработчик выбора полуфабриката в таблице"""
        selected_items = self.semi_finished_table.selectedItems()
        if not selected_items:
            self.current_semi_finished_id = None
            self.update_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.load_composition_button.setEnabled(False)
            self.name_edit.clear()
            self._clear_composition()
            return
        
        row = selected_items[0].row()
        self.current_semi_finished_id = int(self.semi_finished_table.item(row, 0).text())
        name = self.semi_finished_table.item(row, 1).text()
        
        self.name_edit.setText(name)
        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)
        self.load_composition_button.setEnabled(True)
        
        # Автоматически загружаем состав при выборе ПФ
        self._load_composition_from_db(self.current_semi_finished_id)
    
    def _on_ingredient_selection_changed(self):
        """Обработчик выбора ингридиента в списке"""
        self.remove_ingredient_button.setEnabled(len(self.ingredients_list.selectedItems()) > 0)
    
    def _on_add_semi_finished(self):
        """Обработчик добавления полуфабриката"""
        name = self.name_edit.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название полуфабриката")
            return
        
        if db.semi_finished_exists(name):
            QMessageBox.warning(self, "Ошибка", "Полуфабрикат с таким названием уже существует")
            return
        
        # Проверка на пустой состав
        if not self.current_ingredients:
            reply = QMessageBox.question(
                self,
                "Пустой состав",
                "Вы создаете полуфабрикат без ингридиентов. Продолжить?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        try:
            # Создаем полуфабрикат в БД
            semi_finished_id = db.add_semi_finished(name)
            print(f"создание полуфабриката name:{name} id:{semi_finished_id}")
            
            # Сохраняем состав в БД
            if self.current_ingredients:
                for ingredient in self.current_ingredients:
                    db.add_ingredient_to_semi_finished(
                        semi_finished_id,
                        ingredient['id'],
                        ingredient['quantity']
                    )
                print(f"сохранение состава для ПФ id:{semi_finished_id}")
            
            # Очищаем форму
            self.name_edit.clear()
            self._clear_composition()
            self._load_semi_finished()
            
            QMessageBox.information(self, "Успех", f"Полуфабрикат '{name}' добавлен!")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить полуфабрикат: {str(e)}")
    
    def _on_update_semi_finished(self):
        """Обработчик обновления полуфабриката"""
        if not self.current_semi_finished_id:
            return
        
        name = self.name_edit.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название полуфабриката")
            return
        
        if db.semi_finished_exists(name, self.current_semi_finished_id):
            QMessageBox.warning(self, "Ошибка", "Полуфабрикат с таким названием уже существует")
            return
        
        try:
            success = db.update_semi_finished(self.current_semi_finished_id, name)
            
            if success:
                print(f"обновление полуфабриката id:{self.current_semi_finished_id} name:{name}")
                self._load_semi_finished()
                QMessageBox.information(self, "Успех", "Название полуфабриката обновлено!")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось обновить полуфабрикат")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось обновить полуфабрикат: {str(e)}")
    
    def _on_delete_semi_finished(self):
        """Обработчик удаления полуфабриката"""
        if not self.current_semi_finished_id:
            return
        
        try:
            semi_finished = db.get_semi_finished(self.current_semi_finished_id)
            if not semi_finished:
                QMessageBox.warning(self, "Ошибка", "Полуфабрикат не найден")
                return
            
            reply = QMessageBox.question(
                self, 
                "Подтверждение удаления", 
                f"Вы уверены, что хотите удалить полуфабрикат '{semi_finished['name']}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                success = db.delete_semi_finished(self.current_semi_finished_id)
                
                if success:
                    print(f"удаление полуфабриката id:{self.current_semi_finished_id}")
                    self.current_semi_finished_id = None
                    self.name_edit.clear()
                    self.update_button.setEnabled(False)
                    self.delete_button.setEnabled(False)
                    self.load_composition_button.setEnabled(False)
                    self._clear_composition()
                    self._load_semi_finished()
                    QMessageBox.information(self, "Успех", "Полуфабрикат удален!")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить полуфабрикат")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить полуфабрикат: {str(e)}")
    
    def _on_add_ingredient_to_list(self):
        """Обработчик добавления ингридиента в локальный список"""
        if self.ingredient_combo.currentIndex() == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите ингридиент")
            return
        
        ingredient_id = self.ingredient_combo.currentData()
        ingredient_name = self.ingredient_combo.currentText().split(' (')[0]
        quantity = self.quantity_spin.value()
        
        # Проверка на повторное добавление
        for ingredient in self.current_ingredients:
            if ingredient['id'] == ingredient_id:
                QMessageBox.warning(self, "Ошибка", "Этот ингридиент уже добавлен в состав")
                return
        
        # Получаем данные ингридиента из БД
        try:
            ingredient_data = db.get_ingredient(ingredient_id)
            if not ingredient_data:
                QMessageBox.warning(self, "Ошибка", "Ингридиент не найден в базе")
                return
            
            # Добавляем в локальный список
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
            
            # Добавляем в список отображения
            item = QListWidgetItem(
                f"{ingredient_name} - {quantity}г "
                f"(К:{ingredient_data['calories']} Б:{ingredient_data['proteins']} "
                f"Ж:{ingredient_data['fats']} У:{ingredient_data['carbs']})"
            )
            item.setData(Qt.ItemDataRole.UserRole, ingredient_id)
            self.ingredients_list.addItem(item)
            
            print(f"добавление ингридиента в список: {ingredient_name} - {quantity}г")
            
            # Пересчитываем КБЖУ
            self._calculate_and_display_nutrition()
            
            # Сбрасываем количество к значению по умолчанию
            self.quantity_spin.setValue(100)
            
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
        
        # Удаляем из локального списка
        self.current_ingredients = [ing for ing in self.current_ingredients if ing['id'] != ingredient_id]
        
        # Удаляем из списка отображения
        self.ingredients_list.takeItem(self.ingredients_list.row(item))
        
        print(f"удаление ингридиента из списка: {ingredient_name}")
        
        # Пересчитываем КБЖУ
        self._calculate_and_display_nutrition()
    
    def _on_save_composition(self):
        """Обработчик сохранения состава в БД"""
        if not self.current_semi_finished_id:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите или создайте полуфабрикат")
            return
        
        if not self.current_ingredients:
            QMessageBox.warning(self, "Ошибка", "Нельзя сохранить пустой состав")
            return
        
        try:
            # Удаляем старый состав из БД
            old_ingredients = db.get_semi_finished_ingredients(self.current_semi_finished_id)
            for old_ing in old_ingredients:
                db.remove_ingredient_from_semi_finished(self.current_semi_finished_id, old_ing['id'])
            
            # Сохраняем новый состав в БД
            for ingredient in self.current_ingredients:
                success = db.add_ingredient_to_semi_finished(
                    self.current_semi_finished_id,
                    ingredient['id'],
                    ingredient['quantity']
                )
                if not success:
                    raise Exception(f"Не удалось добавить ингридиент {ingredient['name']}")
            
            print(f"сохранение состава для ПФ id:{self.current_semi_finished_id}")
            QMessageBox.information(self, "Успех", "Состав полуфабриката сохранен в БД!")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить состав: {str(e)}")
    
    def _on_load_composition(self):
        """Обработчик загрузки состава из БД"""
        if not self.current_semi_finished_id:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите полуфабрикат")
            return
        
        try:
            self._load_composition_from_db(self.current_semi_finished_id)
            QMessageBox.information(self, "Успех", "Состав загружен из БД!")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить состав: {str(e)}")