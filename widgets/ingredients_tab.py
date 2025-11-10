from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QTableWidget, 
                            QTableWidgetItem, QHeaderView, QGroupBox,
                            QMessageBox, QScrollArea)
from PyQt6.QtCore import Qt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db

class IngredientsTab(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._load_ingredients()
    
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        title_label = QLabel("Управление ингридиентами")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title_label)
        
        content_layout = QHBoxLayout()
        
        left_panel = QWidget()
        left_panel.setMaximumWidth(400)
        left_layout = QVBoxLayout(left_panel)
        
        self._create_add_group(left_layout)
        
        self._create_update_group(left_layout)
        
        self._create_delete_group(left_layout)
        
        content_layout.addWidget(left_panel)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        self._create_ingredients_table(right_layout)
        
        content_layout.addWidget(right_panel, 1)
        
        main_layout.addLayout(content_layout)
    
    def _create_add_group(self, layout):
        group = QGroupBox("Добавление ингридиента")
        group_layout = QVBoxLayout(group)
        
        self.add_name_edit = QLineEdit()
        self.add_name_edit.setPlaceholderText("Название ингридиента")
        group_layout.addWidget(QLabel("Название:"))
        group_layout.addWidget(self.add_name_edit)
        
        nutrients_layout = QHBoxLayout()
        
        self.add_calories_edit = QLineEdit()
        self.add_calories_edit.setPlaceholderText("ккал")
        nutrients_layout.addWidget(QLabel("Калории:"))
        nutrients_layout.addWidget(self.add_calories_edit)
        
        self.add_proteins_edit = QLineEdit()
        self.add_proteins_edit.setPlaceholderText("г")
        nutrients_layout.addWidget(QLabel("Белки:"))
        nutrients_layout.addWidget(self.add_proteins_edit)
        
        group_layout.addLayout(nutrients_layout)
        
        nutrients_layout2 = QHBoxLayout()
        
        self.add_fats_edit = QLineEdit()
        self.add_fats_edit.setPlaceholderText("г")
        nutrients_layout2.addWidget(QLabel("Жиры:"))
        nutrients_layout2.addWidget(self.add_fats_edit)
        
        self.add_carbs_edit = QLineEdit()
        self.add_carbs_edit.setPlaceholderText("г")
        nutrients_layout2.addWidget(QLabel("Углеводы:"))
        nutrients_layout2.addWidget(self.add_carbs_edit)
        
        group_layout.addLayout(nutrients_layout2)
        
        # Кнопка добавления
        add_button = QPushButton("Добавить ингридиент")
        add_button.clicked.connect(self._on_add_ingredient)
        group_layout.addWidget(add_button)
        
        layout.addWidget(group)
    
    def _create_update_group(self, layout):
        group = QGroupBox("Обновление ингридиента")
        group_layout = QVBoxLayout(group)
        
        self.update_id_edit = QLineEdit()
        self.update_id_edit.setPlaceholderText("ID ингридиента")
        group_layout.addWidget(QLabel("ID:"))
        group_layout.addWidget(self.update_id_edit)
        
        self.update_name_edit = QLineEdit()
        self.update_name_edit.setPlaceholderText("Новое название")
        group_layout.addWidget(QLabel("Название:"))
        group_layout.addWidget(self.update_name_edit)
        
        nutrients_layout = QHBoxLayout()
        
        self.update_calories_edit = QLineEdit()
        self.update_calories_edit.setPlaceholderText("ккал")
        nutrients_layout.addWidget(QLabel("Калории:"))
        nutrients_layout.addWidget(self.update_calories_edit)
        
        self.update_proteins_edit = QLineEdit()
        self.update_proteins_edit.setPlaceholderText("г")
        nutrients_layout.addWidget(QLabel("Белки:"))
        nutrients_layout.addWidget(self.update_proteins_edit)
        
        group_layout.addLayout(nutrients_layout)
        
        nutrients_layout2 = QHBoxLayout()
        
        self.update_fats_edit = QLineEdit()
        self.update_fats_edit.setPlaceholderText("г")
        nutrients_layout2.addWidget(QLabel("Жиры:"))
        nutrients_layout2.addWidget(self.update_fats_edit)
        
        self.update_carbs_edit = QLineEdit()
        self.update_carbs_edit.setPlaceholderText("г")
        nutrients_layout2.addWidget(QLabel("Углеводы:"))
        nutrients_layout2.addWidget(self.update_carbs_edit)
        
        group_layout.addLayout(nutrients_layout2)
        
        update_button = QPushButton("Обновить ингридиент")
        update_button.clicked.connect(self._on_update_ingredient)
        group_layout.addWidget(update_button)
        
        layout.addWidget(group)
    
    def _create_delete_group(self, layout):
        group = QGroupBox("Удаление ингридиента")
        group_layout = QVBoxLayout(group)
        
        self.delete_id_edit = QLineEdit()
        self.delete_id_edit.setPlaceholderText("ID ингридиента")
        group_layout.addWidget(QLabel("ID для удаления:"))
        group_layout.addWidget(self.delete_id_edit)
        
        delete_button = QPushButton("Удалить ингридиент")
        delete_button.clicked.connect(self._on_delete_ingredient)
        delete_button.setStyleSheet("background-color: #ff6b6b; color: white;")
        group_layout.addWidget(delete_button)
        
        layout.addWidget(group)
    
    def _create_ingredients_table(self, layout):
        self.table_label = QLabel("Список ингридиентов:")
        self.table_label.setStyleSheet("font-weight: bold; margin: 5px;")
        layout.addWidget(self.table_label)
        
        self.ingredients_table = QTableWidget()
        self.ingredients_table.setColumnCount(7)
        self.ingredients_table.setHorizontalHeaderLabels([
            "ID", "Название", "Калории", "кДж", "Белки", "Жиры", "Углеводы"
        ])
        
        header = self.ingredients_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)
        
        layout.addWidget(self.ingredients_table)
    
    def _load_ingredients(self):
        """Загрузка данных из БД и отображение в таблице"""
        try:
            ingredients = db.get_all_ingredients()
            self.ingredients_table.setRowCount(len(ingredients))
            
            for row, ingredient in enumerate(ingredients):
                self.ingredients_table.setItem(row, 0, QTableWidgetItem(str(ingredient[0])))  # ID
                self.ingredients_table.setItem(row, 1, QTableWidgetItem(str(ingredient[1])))  # Название
                self.ingredients_table.setItem(row, 2, QTableWidgetItem(str(ingredient[2])))  # Калории
                self.ingredients_table.setItem(row, 3, QTableWidgetItem(str(ingredient[3])))  # кДж
                self.ingredients_table.setItem(row, 4, QTableWidgetItem(str(ingredient[4])))  # Белки
                self.ingredients_table.setItem(row, 5, QTableWidgetItem(str(ingredient[5])))  # Жиры
                self.ingredients_table.setItem(row, 6, QTableWidgetItem(str(ingredient[6])))  # Углеводы
            
            self.table_label.setText(f"Список ингридиентов (всего: {len(ingredients)})")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}")
    
    def _on_add_ingredient(self):
        """Обработчик добавления ингридиента"""
        try:
            name = self.add_name_edit.text().strip()
            calories = self.add_calories_edit.text().strip()
            proteins = self.add_proteins_edit.text().strip()
            fats = self.add_fats_edit.text().strip()
            carbs = self.add_carbs_edit.text().strip()
            
            if not name:
                QMessageBox.warning(self, "Ошибка", "Введите название ингридиента")
                return
        
            if db.ingredient_exists(name):
                QMessageBox.warning(self, "Ошибка", "Ингридиент с таким названием уже существует")
                return
            
            try:
                calories_val = float(calories) if calories else 0.0
                proteins_val = float(proteins) if proteins else 0.0
                fats_val = float(fats) if fats else 0.0
                carbs_val = float(carbs) if carbs else 0.0
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Некорректные числовые значения")
                return
            
            print(f"создание элемента name:{name} К:{calories_val} Б:{proteins_val} Ж:{fats_val} У:{carbs_val}")
            
            ingredient_id = db.add_ingredient(
                name=name,
                calories=calories_val,
                proteins=proteins_val,
                fats=fats_val,
                carbs=carbs_val
            )
            
            self.add_name_edit.clear()
            self.add_calories_edit.clear()
            self.add_proteins_edit.clear()
            self.add_fats_edit.clear()
            self.add_carbs_edit.clear()
            
            self._load_ingredients()
            
            QMessageBox.information(self, "Успех", f"Ингридиент '{name}' добавлен с ID {ingredient_id}!")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить ингридиент: {str(e)}")
    
    def _on_update_ingredient(self):
        """Обработчик обновления ингридиента"""
        try:
            ingredient_id = self.update_id_edit.text().strip()
            name = self.update_name_edit.text().strip()
            calories = self.update_calories_edit.text().strip()
            proteins = self.update_proteins_edit.text().strip()
            fats = self.update_fats_edit.text().strip()
            carbs = self.update_carbs_edit.text().strip()
            
            if not ingredient_id:
                QMessageBox.warning(self, "Ошибка", "Введите ID ингридиента")
                return
            
            existing_ingredient = db.get_ingredient(int(ingredient_id))
            if not existing_ingredient:
                QMessageBox.warning(self, "Ошибка", f"Ингридиент с ID {ingredient_id} не найден")
                return
            
            if not any([name, calories, proteins, fats, carbs]):
                QMessageBox.warning(self, "Ошибка", "Заполните хотя бы одно поле для обновления")
                return
            
            if name and db.ingredient_exists(name, int(ingredient_id)):
                QMessageBox.warning(self, "Ошибка", "Ингридиент с таким названием уже существует")
                return
            
            try:
                calories_val = float(calories) if calories else None
                proteins_val = float(proteins) if proteins else None
                fats_val = float(fats) if fats else None
                carbs_val = float(carbs) if carbs else None
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Некорректные числовые значения")
                return
            
            print(f"обновление элемента id:{ingredient_id} name:{name} К:{calories_val} Б:{proteins_val} Ж:{fats_val} У:{carbs_val}")
            
            success = db.update_ingredient(
                ingredient_id=int(ingredient_id),
                name=name if name else None,
                calories=calories_val,
                proteins=proteins_val,
                fats=fats_val,
                carbs=carbs_val
            )
            
            if not success:
                QMessageBox.warning(self, "Ошибка", "Не удалось обновить ингридиент")
                return
            
            self.update_id_edit.clear()
            self.update_name_edit.clear()
            self.update_calories_edit.clear()
            self.update_proteins_edit.clear()
            self.update_fats_edit.clear()
            self.update_carbs_edit.clear()
            
            self._load_ingredients()
            
            QMessageBox.information(self, "Успех", "Ингридиент обновлен!")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось обновить ингридиент: {str(e)}")
    
    def _on_delete_ingredient(self):
        """Обработчик удаления ингридиента"""
        try:
            ingredient_id = self.delete_id_edit.text().strip()
            
            if not ingredient_id:
                QMessageBox.warning(self, "Ошибка", "Введите ID ингридиента")
                return
            
            existing_ingredient = db.get_ingredient(int(ingredient_id))
            if not existing_ingredient:
                QMessageBox.warning(self, "Ошибка", f"Ингридиент с ID {ingredient_id} не найден")
                return
            
            reply = QMessageBox.question(
                self, 
                "Подтверждение удаления", 
                f"Вы уверены, что хотите удалить ингридиент '{existing_ingredient['name']}' с ID {ingredient_id}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                print(f"удаление name:id {ingredient_id}")
                
                success = db.delete_ingredient(int(ingredient_id))
                
                if not success:
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить ингридиент")
                    return
                
                self.delete_id_edit.clear()
                
                self._load_ingredients()
                
                QMessageBox.information(self, "Успех", "Ингридиент удален!")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить ингридиент: {str(e)}")