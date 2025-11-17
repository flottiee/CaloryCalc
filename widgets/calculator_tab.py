from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QGroupBox, QMessageBox,
                            QComboBox, QListWidget, QListWidgetItem, QDoubleSpinBox,
                            QTabWidget, QTextEdit, QSplitter, QFileDialog)
from PyQt6.QtGui import QPixmap
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db

class CalculatorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.current_ingredients = []
        self.current_semi_finished = []
        self.current_products = []
        self._setup_ui()
        self._load_data()
    
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        hbox = QHBoxLayout()
        title_label = QLabel("Калькулятор калорий")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        hbox.addWidget(title_label)
        
        
        self.svg = QSvgWidget(self)
        #self.svg.move(15, 350)
        self.svg.load('1680px.svg')
        self.svg.renderer()
        self.svg.setFixedSize(120, 60)
        hbox.addWidget(self.svg)

        main_layout.addLayout(hbox)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        left_panel = self._create_search_panel()
        splitter.addWidget(left_panel)
        
        right_panel = self._create_recipe_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([400, 600])
        main_layout.addWidget(splitter)
    
    def _create_search_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        search_group = QGroupBox("Поиск компонентов")
        search_layout = QVBoxLayout(search_group)
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Введите название ингредиента, полуфабриката или продукта...")
        self.search_edit.textChanged.connect(self._on_search)
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.search_edit)
        
        self.search_tabs = QTabWidget()
        
        ingredients_tab = QWidget()
        ingredients_layout = QVBoxLayout(ingredients_tab)
        self.ingredients_search_list = QListWidget()
        self.ingredients_search_list.itemDoubleClicked.connect(self._on_add_ingredient_from_search)
        ingredients_layout.addWidget(QLabel("Ингредиенты:"))
        ingredients_layout.addWidget(self.ingredients_search_list)
        self.search_tabs.addTab(ingredients_tab, "Ингредиенты")
        
        semi_finished_tab = QWidget()
        sf_layout = QVBoxLayout(semi_finished_tab)
        self.sf_search_list = QListWidget()
        self.sf_search_list.itemDoubleClicked.connect(self._on_add_semi_finished_from_search)
        sf_layout.addWidget(QLabel("Полуфабрикаты:"))
        sf_layout.addWidget(self.sf_search_list)
        self.search_tabs.addTab(semi_finished_tab, "Полуфабрикаты")
        
        products_tab = QWidget()
        products_layout = QVBoxLayout(products_tab)
        self.products_search_list = QListWidget()
        self.products_search_list.itemDoubleClicked.connect(self._on_add_product_from_search)
        products_layout.addWidget(QLabel("Продукты (как шаблоны):"))
        products_layout.addWidget(self.products_search_list)
        self.search_tabs.addTab(products_tab, "Продукты")
        
        search_layout.addWidget(self.search_tabs)
        
        quick_add_group = QGroupBox("Быстрое добавление")
        quick_layout = QVBoxLayout(quick_add_group)
        
        type_layout = QHBoxLayout()
        self.quick_type_combo = QComboBox()
        self.quick_type_combo.addItem("Ингредиент", "ingredient")
        self.quick_type_combo.addItem("Полуфабрикат", "semi_finished") 
        self.quick_type_combo.addItem("Продукт", "product")
        type_layout.addWidget(QLabel("Тип компонента:"))
        type_layout.addWidget(self.quick_type_combo)
        quick_layout.addLayout(type_layout)
        
        component_layout = QHBoxLayout()
        self.quick_component_combo = QComboBox()
        component_layout.addWidget(QLabel("Компонент:"))
        component_layout.addWidget(self.quick_component_combo, 1)
        quick_layout.addLayout(component_layout)
        
        weight_layout = QHBoxLayout()
        self.quick_weight_spin = QDoubleSpinBox()
        self.quick_weight_spin.setRange(1, 10000)
        self.quick_weight_spin.setValue(100)
        self.quick_weight_spin.setSuffix(" г")
        self.quick_weight_spin.setSingleStep(10)
        weight_layout.addWidget(QLabel("Вес:"))
        weight_layout.addWidget(self.quick_weight_spin)
        quick_layout.addLayout(weight_layout)
        
        self.quick_add_btn = QPushButton("Добавить в рецепт")
        self.quick_add_btn.clicked.connect(self._on_quick_add)
        quick_layout.addWidget(self.quick_add_btn)
        
        self.quick_type_combo.currentIndexChanged.connect(self._update_quick_component_list)
        
        layout.addWidget(search_group)
        layout.addWidget(quick_add_group)
        self._update_quick_component_list()
        
        return panel
    
    def _create_recipe_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        info_group = QGroupBox("Информация о рецепте")
        info_layout = QVBoxLayout(info_group)
        
        info_layout.addWidget(QLabel("Название рецепта:"))
        self.recipe_name_edit = QLineEdit()
        self.recipe_name_edit.setPlaceholderText("Введите название рецепта...")
        info_layout.addWidget(self.recipe_name_edit)
        
        info_layout.addWidget(QLabel("Описание:"))
        self.recipe_description_edit = QTextEdit()
        self.recipe_description_edit.setMaximumHeight(80)
        self.recipe_description_edit.setPlaceholderText("Описание рецепта...")
        info_layout.addWidget(self.recipe_description_edit)
        
        layout.addWidget(info_group)
        
        composition_group = QGroupBox("Состав рецепта")
        composition_layout = QVBoxLayout(composition_group)
        
        self.composition_tabs = QTabWidget()
        
        ingredients_tab = QWidget()
        ingredients_layout = QVBoxLayout(ingredients_tab)
        self.ingredients_list = QListWidget()
        self.ingredients_list.itemDoubleClicked.connect(self._on_remove_ingredient)
        ingredients_layout.addWidget(QLabel("Ингредиенты:"))
        ingredients_layout.addWidget(self.ingredients_list)
        self.composition_tabs.addTab(ingredients_tab, "Ингредиенты")
        
        sf_tab = QWidget()
        sf_layout = QVBoxLayout(sf_tab)
        self.semi_finished_list = QListWidget()
        self.semi_finished_list.itemDoubleClicked.connect(self._on_remove_semi_finished)
        sf_layout.addWidget(QLabel("Полуфабрикаты:"))
        sf_layout.addWidget(self.semi_finished_list)
        self.composition_tabs.addTab(sf_tab, "Полуфабрикаты")
        
        products_tab = QWidget()
        products_layout = QVBoxLayout(products_tab)
        self.products_list = QListWidget()
        self.products_list.itemDoubleClicked.connect(self._on_remove_product)
        products_layout.addWidget(QLabel("Продукты:"))
        products_layout.addWidget(self.products_list)
        self.composition_tabs.addTab(products_tab, "Продукты")
        
        composition_layout.addWidget(self.composition_tabs)
        
        composition_buttons_layout = QHBoxLayout()
        
        self.clear_btn = QPushButton("Очистить состав")
        self.clear_btn.clicked.connect(self._on_clear_composition)
        self.clear_btn.setStyleSheet("background-color: #ff6b6b; color: white;")
        composition_buttons_layout.addWidget(self.clear_btn)
        
        self.load_template_btn = QPushButton("Загрузить как шаблон")
        self.load_template_btn.clicked.connect(self._on_load_template)
        composition_buttons_layout.addWidget(self.load_template_btn)
        
        composition_layout.addLayout(composition_buttons_layout)
        
        layout.addWidget(composition_group)
        
        nutrition_group = QGroupBox("Расчет пищевой ценности")
        nutrition_layout = QVBoxLayout(nutrition_group)
        
        self.nutrition_label = QLabel("Добавьте компоненты для расчета")
        self.nutrition_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        nutrition_layout.addWidget(self.nutrition_label)
        
        self.detailed_nutrition_label = QLabel("")
        self.detailed_nutrition_label.setStyleSheet("font-size: 12px; color: #555;")
        nutrition_layout.addWidget(self.detailed_nutrition_label)
        
        layout.addWidget(nutrition_group)
        
        actions_group = QGroupBox("Действия")
        actions_layout = QHBoxLayout(actions_group)
        
        self.calculate_btn = QPushButton("Рассчитать")
        self.calculate_btn.clicked.connect(self._on_calculate)
        self.calculate_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        actions_layout.addWidget(self.calculate_btn)
        
        self.export_btn = QPushButton("Экспорт")
        self.export_btn.clicked.connect(self._on_export)
        self.export_btn.setStyleSheet("background-color: #2196F3; color: white;")
        actions_layout.addWidget(self.export_btn)
        
        self.save_btn = QPushButton("Сохранить рецепт")
        self.save_btn.clicked.connect(self._on_save_recipe)
        self.save_btn.setStyleSheet("background-color: #FF9800; color: white;")
        actions_layout.addWidget(self.save_btn)
        
        layout.addWidget(actions_group)
        
        return panel
    
    def _load_data(self):
        """Загрузка данных для поиска"""
        self._on_search()
        self._update_quick_component_list()  
        
    def _on_search(self):
        """Обработчик поиска"""
        search_term = self.search_edit.text().strip()
        
        ingredients = db.search_ingredients(search_term) if search_term else db.get_all_ingredients()
        self.ingredients_search_list.clear()
        for ingredient in ingredients:
            item = QListWidgetItem(
                f"{ingredient[1]} (К:{ingredient[2]} Б:{ingredient[4]} Ж:{ingredient[5]} У:{ingredient[6]})"
            )
            item.setData(Qt.ItemDataRole.UserRole, ("ingredient", ingredient[0]))
            self.ingredients_search_list.addItem(item)
        
        semi_finished = db.get_all_semi_finished()
        self.sf_search_list.clear()
        for sf in semi_finished:
            if not search_term or search_term.lower() in sf[1].lower():
                nutrition = db.calculate_semi_finished_nutrition(sf[0])
                item = QListWidgetItem(
                    f"{sf[1]} (К:{nutrition['calories']} Б:{nutrition['proteins']} Ж:{nutrition['fats']} У:{nutrition['carbs']})"
                )
                item.setData(Qt.ItemDataRole.UserRole, ("semi_finished", sf[0]))
                self.sf_search_list.addItem(item)
        
        products = db.get_all_products()
        self.products_search_list.clear()
        for product in products:
            if not search_term or search_term.lower() in product[1].lower():
                nutrition = db.calculate_product_nutrition(product[0])
                item = QListWidgetItem(
                    f"{product[1]} (К:{nutrition['calories']} Б:{nutrition['proteins']} Ж:{nutrition['fats']} У:{nutrition['carbs']})"
                )
                item.setData(Qt.ItemDataRole.UserRole, ("product", product[0]))
                self.products_search_list.addItem(item)
    
    def _on_add_ingredient_from_search(self, item):
        """Добавление ингредиента из поиска"""
        component_type, component_id = item.data(Qt.ItemDataRole.UserRole)
        component_name = item.text().split(' (')[0]
        
        ingredient_data = db.get_ingredient(component_id)
        if ingredient_data:
            self.current_ingredients.append({
                'id': component_id,
                'name': component_name,
                'quantity': 100,
                'calories': ingredient_data['calories'],
                'proteins': ingredient_data['proteins'],
                'fats': ingredient_data['fats'],
                'carbs': ingredient_data['carbs']
            })
            self._update_composition_display()
    
    def _on_add_semi_finished_from_search(self, item):
        """Добавление полуфабриката из поиска"""
        component_type, component_id = item.data(Qt.ItemDataRole.UserRole)
        component_name = item.text().split(' (')[0]
        
        self.current_semi_finished.append({
            'id': component_id,
            'name': component_name,
            'quantity': 100
        })
        self._update_composition_display()
    
    def _on_add_product_from_search(self, item):
        """Добавление продукта из поиска (как шаблона)"""
        component_type, component_id = item.data(Qt.ItemDataRole.UserRole)
        component_name = item.text().split(' (')[0]
        
        ingredients = db.get_product_ingredients(component_id)
        semi_finished = db.get_product_semi_finished(component_id)
        
        for ingredient in ingredients:
            self.current_ingredients.append({
                'id': ingredient['id'],
                'name': ingredient['name'],
                'quantity': ingredient['quantity'],
                'calories': ingredient['calories'],
                'proteins': ingredient['proteins'],
                'fats': ingredient['fats'],
                'carbs': ingredient['carbs']
            })
        
        for sf in semi_finished:
            self.current_semi_finished.append({
                'id': sf['id'],
                'name': sf['name'],
                'quantity': sf['quantity']
            })
        
        self._update_composition_display()
        QMessageBox.information(self, "Шаблон загружен", f"Состав продукта '{component_name}' загружен как шаблон!")
    
    def _on_quick_add(self):
        """Быстрое добавление выбранного компонента"""
        pass
    
    def _update_composition_display(self):
        """Обновление отображения состава"""
        self.ingredients_list.clear()
        for ingredient in self.current_ingredients:
            item = QListWidgetItem(f"{ingredient['name']} - {ingredient['quantity']}г")
            self.ingredients_list.addItem(item)
        
        self.semi_finished_list.clear()
        for sf in self.current_semi_finished:
            item = QListWidgetItem(f"{sf['name']} - {sf['quantity']}г")
            self.semi_finished_list.addItem(item)
        
        self.products_list.clear()
        for product in self.current_products:
            item = QListWidgetItem(f"{product['name']} - {product['quantity']}г")
            self.products_list.addItem(item)
    
    def _on_remove_ingredient(self, item):
        """Удаление ингредиента из состава"""
        row = self.ingredients_list.row(item)
        if row >= 0:
            removed = self.current_ingredients.pop(row)
            self._update_composition_display()
    
    def _on_remove_semi_finished(self, item):
        """Удаление полуфабриката из состава"""
        row = self.semi_finished_list.row(item)
        if row >= 0:
            removed = self.current_semi_finished.pop(row)
            self._update_composition_display()
    
    def _on_remove_product(self, item):
        """Удаление продукта из состава"""
        row = self.products_list.row(item)
        if row >= 0:
            removed = self.current_products.pop(row)
            self._update_composition_display()
    
    def _on_clear_composition(self):
        """Очистка состава"""
        self.current_ingredients.clear()
        self.current_semi_finished.clear()
        self.current_products.clear()
        self._update_composition_display()
        self.nutrition_label.setText("Добавьте компоненты для расчета")
        self.detailed_nutrition_label.setText("")
    
    def _on_load_template(self):
        """Загрузка шаблона из существующего продукта"""
        pass
    
    def _on_calculate(self):
        """Расчет пищевой ценности"""
        if not self.current_ingredients and not self.current_semi_finished:
            QMessageBox.warning(self, "Ошибка", "Добавьте компоненты для расчета!")
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
            QMessageBox.warning(self, "Ошибка", "Общий вес не может быть нулевым!")
            return
        
        factor_to_100g = 100.0 / total_weight
        
        nutrition_per_100g = {
            'calories': round(total_calories * factor_to_100g, 2),
            'kJoule': round(total_kJoule * factor_to_100g, 2),
            'proteins': round(total_proteins * factor_to_100g, 2),
            'fats': round(total_fats * factor_to_100g, 2),
            'carbs': round(total_carbs * factor_to_100g, 2)
        }
        
        total_nutrition = {
            'calories': round(total_calories, 2),
            'kJoule': round(total_kJoule, 2),
            'proteins': round(total_proteins, 2),
            'fats': round(total_fats, 2),
            'carbs': round(total_carbs, 2)
        }
        
        self.nutrition_label.setText(
            f"КБЖУ на 100г: К:{nutrition_per_100g['calories']} "
            f"Б:{nutrition_per_100g['proteins']} Ж:{nutrition_per_100g['fats']} У:{nutrition_per_100g['carbs']}"
        )
        
        detailed_text = (
            f"Общий вес: {total_weight}г\n"
            f"Общая пищевая ценность:\n"
            f"  Калории: {total_nutrition['calories']} ккал ({total_nutrition['kJoule']} кДж)\n"
            f"  Белки: {total_nutrition['proteins']}г\n"
            f"  Жиры: {total_nutrition['fats']}г\n"
            f"  Углеводы: {total_nutrition['carbs']}г"
        )
        self.detailed_nutrition_label.setText(detailed_text)
    
    def _on_export(self):
        """Экспорт рецепта в текстовый файл"""
        if not self.current_ingredients and not self.current_semi_finished:
            QMessageBox.warning(self, "Ошибка", "Нет данных для экспорта!")
            return
        self._on_calculate()
        
        export_content = self._generate_export_content()
        
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Все файлы (*);;Текстовые файлы (*.txt)")

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"{export_content}")
        else:
            print("fuck")

        QMessageBox.information(self, "Экспорт", 
            "этикетка экспортированна в выбранную папку")

    def _generate_export_content(self):
        """Генерирует форматированное содержимое для экспорта"""
        
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
            return "Ошибка: общий вес не может быть нулевым!"
        
        factor_to_100g = 100.0 / total_weight
        
        nutrition_per_100g = {
            'calories': round(total_calories * factor_to_100g, 2),
            'kJoule': round(total_kJoule * factor_to_100g, 2),
            'proteins': round(total_proteins * factor_to_100g, 2),
            'fats': round(total_fats * factor_to_100g, 2),
            'carbs': round(total_carbs * factor_to_100g, 2)
        }
        
        total_nutrition = {
            'calories': round(total_calories, 2),
            'kJoule': round(total_kJoule, 2),
            'proteins': round(total_proteins, 2),
            'fats': round(total_fats, 2),
            'carbs': round(total_carbs, 2)
        }
        
        content = []
        
        recipe_name = self.recipe_name_edit.text().strip() or "Без названия"
        content.append("=" * 27)
        content.append(f"РЕЦЕПТ: {recipe_name}")
        content.append("=" * 27)
        content.append("\n")
        
        description = self.recipe_description_edit.toPlainText().strip()
        if description:
            content.append("ОПИСАНИЕ:\n")
            content.append(description)
            content.append("\n")
        
        content.append("СОСТАВ РЕЦЕПТА:\n")
        content.append("-" * 27)
        
        if self.current_ingredients:
            content.append("ИНГРЕДИЕНТЫ:\n")
            for i, ingredient in enumerate(self.current_ingredients, 1):
                content.append(f"{i:2d}. {ingredient['name']}: {ingredient['quantity']} г")
            content.append("\n")
        
        if self.current_semi_finished:
            content.append("ПОЛУФАБРИКАТЫ:\n")
            for i, sf in enumerate(self.current_semi_finished, 1):
                content.append(f"{i:2d}. {sf['name']}: {sf['quantity']} г")
            content.append("\n")
        
        content.append("ПИЩЕВАЯ ЦЕННОСТЬ:\n")
        content.append("-" * 27)
        
        content.append(f"На 100 г продукта:")
        content.append(f"  Калории: {nutrition_per_100g['calories']} ккал ({nutrition_per_100g['kJoule']} кДж)")
        content.append(f"  Белки: {nutrition_per_100g['proteins']} г")
        content.append(f"  Жиры: {nutrition_per_100g['fats']} г") 
        content.append(f"  Углеводы: {nutrition_per_100g['carbs']} г")
        content.append("\n")
        
        content.append(f"ОБЩАЯ (вес: {total_weight} г):\n")
        content.append(f"  Калории: {total_nutrition['calories']} ккал ({total_nutrition['kJoule']} кДж)")
        content.append(f"  Белки: {total_nutrition['proteins']} г")
        content.append(f"  Жиры: {total_nutrition['fats']} г")
        content.append(f"  Углеводы: {total_nutrition['carbs']} г")
        content.append("\n")
        
        content.append("РАСПРЕДЕЛЕНИЕ КАЛОРИЙ:\n")
        content.append("-" * 27)
        protein_calories = total_nutrition['proteins'] * 4
        fat_calories = total_nutrition['fats'] * 9
        carb_calories = total_nutrition['carbs'] * 4
        total_cal_from_macros = protein_calories + fat_calories + carb_calories
        
        if total_cal_from_macros > 0:
            protein_percent = (protein_calories / total_cal_from_macros) * 100
            fat_percent = (fat_calories / total_cal_from_macros) * 100
            carb_percent = (carb_calories / total_cal_from_macros) * 100
            
            content.append(f"Белки: {protein_calories:.1f} ккал ({protein_percent:.1f}%)")
            content.append(f"Жиры: {fat_calories:.1f} ккал ({fat_percent:.1f}%)")
            content.append(f"Углеводы: {carb_calories:.1f} ккал ({carb_percent:.1f}%)")
        else:
            content.append("Недостаточно данных для распределения")
        
        content.append("\n")
        content.append("=" * 27)
        content.append(f"Сгенерировано: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        content.append("=" * 27)
        
        return "\n".join(content)
    
    def _on_save_recipe(self):
        """Сохранение рецепта как продукта"""
        name = self.recipe_name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название рецепта!")
            return
        
        if not self.current_ingredients and not self.current_semi_finished:
            QMessageBox.warning(self, "Ошибка", "Рецепт не может быть пустым!")
            return
        
        try:
            product_id = db.add_product(name)
            
            for ingredient in self.current_ingredients:
                db.add_ingredient_to_product(product_id, ingredient['id'], ingredient['quantity'])
            
            for sf in self.current_semi_finished:
                db.add_semi_finished_to_product(product_id, sf['id'], sf['quantity'])
            
            QMessageBox.information(self, "Успех", f"Рецепт '{name}' сохранен как продукт!")
            
            self.recipe_name_edit.clear()
            self.recipe_description_edit.clear()
            self._on_clear_composition()
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить рецепт: {str(e)}")
    
    def _update_quick_component_list(self):
        """Обновляет список компонентов для быстрого добавления"""
        component_type = self.quick_type_combo.currentData()
        self.quick_component_combo.clear()
        
        if component_type == "ingredient":
            ingredients = db.get_all_ingredients()
            for ingredient in ingredients:
                self.quick_component_combo.addItem(
                    f"{ingredient[1]} (К:{ingredient[2]} Б:{ingredient[4]} Ж:{ingredient[5]} У:{ingredient[6]})",
                    ingredient[0] 
                )
        
        elif component_type == "semi_finished":
            semi_finished = db.get_all_semi_finished()
            for sf in semi_finished:
                nutrition = db.calculate_semi_finished_nutrition(sf[0])
                self.quick_component_combo.addItem(
                    f"{sf[1]} (К:{nutrition['calories']} Б:{nutrition['proteins']} Ж:{nutrition['fats']} У:{nutrition['carbs']})",
                    sf[0]
                )
        
        elif component_type == "product":
            products = db.get_all_products()
            for product in products:
                nutrition = db.calculate_product_nutrition(product[0])
                self.quick_component_combo.addItem(
                    f"{product[1]} (К:{nutrition['calories']} Б:{nutrition['proteins']} Ж:{nutrition['fats']} У:{nutrition['carbs']})",
                    product[0]  
                )

    def _on_quick_add(self):
        """Обработчик быстрого добавления компонента"""
        if self.quick_component_combo.currentIndex() == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите компонент для добавления")
            return
        
        component_type = self.quick_type_combo.currentData()
        component_id = self.quick_component_combo.currentData()
        component_name = self.quick_component_combo.currentText().split(' (')[0]
        weight = self.quick_weight_spin.value()
        
        try:
            if component_type == "ingredient":
                ingredient_data = db.get_ingredient(component_id)
                if ingredient_data:
                    self.current_ingredients.append({
                        'id': component_id,
                        'name': component_name,
                        'quantity': weight,
                        'calories': ingredient_data['calories'],
                        'proteins': ingredient_data['proteins'],
                        'fats': ingredient_data['fats'],
                        'carbs': ingredient_data['carbs']
                    })
                    print(f"Добавлен ингредиент: {component_name} - {weight}г")
            
            elif component_type == "semi_finished":
                self.current_semi_finished.append({
                    'id': component_id,
                    'name': component_name,
                    'quantity': weight
                })
                print(f"Добавлен полуфабрикат: {component_name} - {weight}г")
            
            elif component_type == "product":
                ingredients = db.get_product_ingredients(component_id)
                semi_finished = db.get_product_semi_finished(component_id)
                
                total_original_weight = sum(ing['quantity'] for ing in ingredients) + sum(sf['quantity'] for sf in semi_finished)
                if total_original_weight > 0:
                    scale_factor = weight / total_original_weight
                    
                    for ingredient in ingredients:
                        scaled_weight = ingredient['quantity'] * scale_factor
                        self.current_ingredients.append({
                            'id': ingredient['id'],
                            'name': ingredient['name'],
                            'quantity': round(scaled_weight, 1),
                            'calories': ingredient['calories'],
                            'proteins': ingredient['proteins'],
                            'fats': ingredient['fats'],
                            'carbs': ingredient['carbs']
                        })
                    
                    for sf in semi_finished:
                        scaled_weight = sf['quantity'] * scale_factor
                        self.current_semi_finished.append({
                            'id': sf['id'],
                            'name': sf['name'],
                            'quantity': round(scaled_weight, 1)
                        })
                    
                    print(f"Добавлен продукт как шаблон: {component_name} - {weight}г (масштабирован)")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось разобрать состав продукта")
                    return
            
            self._update_composition_display()
            self.quick_weight_spin.setValue(100)
            
            QMessageBox.information(self, "Успех", f"Компонент '{component_name}' добавлен в рецепт!\nВес: {weight}г")
            
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить компонент: {str(e)}")

