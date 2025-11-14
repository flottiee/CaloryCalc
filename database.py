import sqlite3
from typing import List, Tuple, Optional, Dict

class IngredientDB:
    def __init__(self, db_path: str = "database.db"):
        self.db_path = db_path
        self._create_tables()
    
    def _get_connection(self):
        """Создает и возвращает соединение с базой данных"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _create_tables(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ingredients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    calories REAL NOT NULL DEFAULT 0,
                    kJoule REAL NOT NULL DEFAULT 0,
                    proteins REAL NOT NULL DEFAULT 0,
                    fats REAL NOT NULL DEFAULT 0,
                    carbs REAL NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS semiFinished (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS semiFinished_ingredients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    semiFinished_id INTEGER NOT NULL,
                    ingredient_id INTEGER NOT NULL,
                    quantity REAL NOT NULL DEFAULT 100,
                    FOREIGN KEY (semiFinished_id) REFERENCES semiFinished (id) ON DELETE CASCADE,
                    FOREIGN KEY (ingredient_id) REFERENCES ingredients (id) ON DELETE CASCADE,
                    UNIQUE(semiFinished_id, ingredient_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products_ingredients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    productId INTEGER NOT NULL,
                    ingredientId INTEGER NOT NULL,
                    quantity REAL NOT NULL DEFAULT 100,
                    FOREIGN KEY (productId) REFERENCES products (id) ON DELETE CASCADE,
                    FOREIGN KEY (ingredientId) REFERENCES ingredients (id) ON DELETE CASCADE,
                    UNIQUE(productId, ingredientId)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products_semiFinished (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    productId INTEGER NOT NULL,
                    semiFinishedId INTEGER NOT NULL,
                    quantity REAL NOT NULL DEFAULT 100,
                    FOREIGN KEY (productId) REFERENCES products (id) ON DELETE CASCADE,
                    FOREIGN KEY (semiFinishedId) REFERENCES semiFinished (id) ON DELETE CASCADE,
                    UNIQUE(productId, semiFinishedId)
                )
            ''')
            
            conn.commit()
    
    # === МЕТОДЫ ДЛЯ ИНГРИДИЕНТОВ ===
    
    def add_ingredient(self, name: str, calories: Optional[float] = None, proteins: float = 0, 
                  fats: float = 0, carbs: float = 0, kJoule: Optional[float] = None) -> int:
        """
        Добавляет новый ингридиент в базу данных
        """
        if calories is None:
            calories = (proteins * 4) + (fats * 9) + (carbs * 4)
        
        if kJoule is None:
            kJoule = calories * 4.184
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO ingredients (name, calories, kJoule, proteins, fats, carbs)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, calories, kJoule, proteins, fats, carbs))
            
            ingredient_id = cursor.lastrowid
            conn.commit()
            return ingredient_id
    
    def get_ingredient(self, ingredient_id: int) -> Optional[dict]:
        """
        Получает ингридиент по ID
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, calories, kJoule, proteins, fats, carbs
                FROM ingredients 
                WHERE id = ?
            ''', (ingredient_id,))
            
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_all_ingredients(self) -> List[Tuple]:
        """
        Получает все ингридиенты из базы данных
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, calories, kJoule, proteins, fats, carbs
                FROM ingredients 
                ORDER BY name
            ''')
            
            return cursor.fetchall()
    
    def update_ingredient(self, ingredient_id: int, name: Optional[str] = None,
                     calories: Optional[float] = None, 
                     proteins: Optional[float] = None,
                     fats: Optional[float] = None,
                     carbs: Optional[float] = None,
                     kJoule: Optional[float] = None) -> bool:
        """
        Обновляет данные ингридиента
        """
        current_data = self.get_ingredient(ingredient_id)
        if not current_data:
            return False
        
        new_calories = calories if calories is not None else current_data['calories']
        new_proteins = proteins if proteins is not None else current_data['proteins']
        new_fats = fats if fats is not None else current_data['fats']
        new_carbs = carbs if carbs is not None else current_data['carbs']
        
        if any([proteins is not None, fats is not None, carbs is not None]):
            new_calories = (new_proteins * 4) + (new_fats * 9) + (new_carbs * 4)
        
        new_kJoule = kJoule if kJoule is not None else new_calories * 4.184
        
        update_fields = []
        update_values = []
        
        if name is not None:
            update_fields.append("name = ?")
            update_values.append(name)
        
        update_fields.append("calories = ?")
        update_values.append(new_calories)
        
        update_fields.append("kJoule = ?")
        update_values.append(new_kJoule)
        
        update_fields.append("proteins = ?")
        update_values.append(new_proteins)
        
        update_fields.append("fats = ?")
        update_values.append(new_fats)
        
        update_fields.append("carbs = ?")
        update_values.append(new_carbs)
        
        update_values.append(ingredient_id)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE ingredients 
                SET {', '.join(update_fields)}
                WHERE id = ?
            ''', update_values)
            
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_ingredient(self, ingredient_id: int) -> bool:
        """
        Удаляет ингридиент по ID
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM ingredients WHERE id = ?', (ingredient_id,))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def search_ingredients(self, search_term: str) -> List[Tuple]:
        """
        Поиск ингридиентов по названию
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, calories, kJoule, proteins, fats, carbs
                FROM ingredients 
                WHERE name LIKE ?
                ORDER BY name
            ''', (f'%{search_term}%',))
            
            return cursor.fetchall()
    
    def ingredient_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """
        Проверяет, существует ли ингридиент с таким названием
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if exclude_id:
                cursor.execute('''
                    SELECT 1 FROM ingredients 
                    WHERE name = ? AND id != ?
                ''', (name, exclude_id))
            else:
                cursor.execute('''
                    SELECT 1 FROM ingredients 
                    WHERE name = ?
                ''', (name,))
            
            return cursor.fetchone() is not None
    
    def get_ingredients_count(self) -> int:
        """
        Возвращает общее количество ингридиентов в базе
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM ingredients')
            return cursor.fetchone()[0]

    # === МЕТОДЫ ДЛЯ ПОЛУФАБРИКАТОВ ===
    
    def add_semi_finished(self, name: str) -> int:
        """
        Добавляет новый полуфабрикат
        
        Args:
            name: Название полуфабриката
        
        Returns:
            ID созданного полуфабриката
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO semiFinished (name)
                VALUES (?)
            ''', (name,))
            
            semi_finished_id = cursor.lastrowid
            conn.commit()
            return semi_finished_id
    
    def get_semi_finished(self, semi_finished_id: int) -> Optional[dict]:
        """
        Получает полуфабрикат по ID
        
        Returns:
            Словарь с данными полуфабриката
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name
                FROM semiFinished 
                WHERE id = ?
            ''', (semi_finished_id,))
            
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_all_semi_finished(self) -> List[Tuple]:
        """
        Получает все полуфабрикаты из базы данных
        
        Returns:
            Список кортежей с данными полуфабрикатов
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name
                FROM semiFinished 
                ORDER BY name
            ''')
            
            return cursor.fetchall()
    
    def update_semi_finished(self, semi_finished_id: int, name: str) -> bool:
        """
        Обновляет название полуфабриката
        
        Returns:
            True если обновление успешно
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE semiFinished 
                SET name = ?
                WHERE id = ?
            ''', (name, semi_finished_id))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_semi_finished(self, semi_finished_id: int) -> bool:
        """
        Удаляет полуфабрикат по ID
        
        Returns:
            True если удаление успешно
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM semiFinished WHERE id = ?', (semi_finished_id,))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def semi_finished_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """
        Проверяет, существует ли полуфабрикат с таким названием
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if exclude_id:
                cursor.execute('''
                    SELECT 1 FROM semiFinished 
                    WHERE name = ? AND id != ?
                ''', (name, exclude_id))
            else:
                cursor.execute('''
                    SELECT 1 FROM semiFinished 
                    WHERE name = ?
                ''', (name,))
            
            return cursor.fetchone() is not None
    
    def get_semi_finished_count(self) -> int:
        """
        Возвращает общее количество полуфабрикатов в базе
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM semiFinished')
            return cursor.fetchone()[0]

    # === МЕТОДЫ ДЛЯ СВЯЗЕЙ ПОЛУФАБРИКАТОВ И ИНГРИДИЕНТОВ ===
    
    def add_ingredient_to_semi_finished(self, semi_finished_id: int, ingredient_id: int, quantity: float = 100) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO semiFinished_ingredients (semiFinished_id, ingredient_id, quantity)
                    VALUES (?, ?, ?)
                ''', (semi_finished_id, ingredient_id, quantity))
                
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False
    
    def remove_ingredient_from_semi_finished(self, semi_finished_id: int, ingredient_id: int) -> bool:
        """
        Удаляет ингридиент из полуфабриката
        
        Returns:
            True если удаление успешно
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM semiFinished_ingredients 
                WHERE semiFinished_id = ? AND ingredient_id = ?
            ''', (semi_finished_id, ingredient_id))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def get_semi_finished_ingredients(self, semi_finished_id: int) -> List[Dict]:
        """
        Получает все ингридиенты полуфабриката с их количеством
        
        Returns:
            Список словарей с данными ингридиентов и их количеством
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT i.id, i.name, i.calories, i.kJoule, i.proteins, i.fats, i.carbs, semiFinished_ingredients.quantity
                FROM semiFinished_ingredients
                JOIN ingredients i ON semiFinished_ingredients.ingredient_id = i.id
                WHERE semiFinished_ingredients.semiFinished_id = ?
                ORDER BY i.name
            ''', (semi_finished_id,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def calculate_semi_finished_nutrition(self, semi_finished_id: int) -> Dict[str, float]:
        """
        Рассчитывает пищевую ценность полуфабриката на 100г
        
        Returns:
            Словарь с рассчитанными значениями КБЖУ
        """
        ingredients = self.get_semi_finished_ingredients(semi_finished_id)
        
        if not ingredients:
            return {'calories': 0, 'kJoule': 0, 'proteins': 0, 'fats': 0, 'carbs': 0}
        
        total_weight = sum(ingredient['quantity'] for ingredient in ingredients)
        
        if total_weight == 0:
            return {'calories': 0, 'kJoule': 0, 'proteins': 0, 'fats': 0, 'carbs': 0}

        total_calories = 0
        total_kJoule = 0
        total_proteins = 0
        total_fats = 0
        total_carbs = 0
        
        for ingredient in ingredients:
            factor = ingredient['quantity'] / 100.0
            total_calories += ingredient['calories'] * factor
            total_kJoule += ingredient['kJoule'] * factor
            total_proteins += ingredient['proteins'] * factor
            total_fats += ingredient['fats'] * factor
            total_carbs += ingredient['carbs'] * factor
        
        factor_to_100g = 100.0 / total_weight
        
        return {
            'calories': round(total_calories * factor_to_100g, 2),
            'kJoule': round(total_kJoule * factor_to_100g, 2),
            'proteins': round(total_proteins * factor_to_100g, 2),
            'fats': round(total_fats * factor_to_100g, 2),
            'carbs': round(total_carbs * factor_to_100g, 2)
        }
    
    # === МЕТОДЫ ДЛЯ ПРОДУКТОВ ===

    def add_product(self, name: str) -> int:
        """
        Добавляет новый продукт
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO products (name)
                VALUES (?)
            ''', (name,))
            
            product_id = cursor.lastrowid
            conn.commit()
            return product_id

    def get_product(self, product_id: int) -> Optional[dict]:
        """
        Получает продукт по ID
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name
                FROM products 
                WHERE id = ?
            ''', (product_id,))
            
            row = cursor.fetchone()
            return dict(row) if row else None

    def product_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """
        Проверяет, существует ли продукт с таким названием
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if exclude_id:
                cursor.execute('''
                    SELECT 1 FROM products 
                    WHERE name = ? AND id != ?
                ''', (name, exclude_id))
            else:
                cursor.execute('''
                    SELECT 1 FROM products 
                    WHERE name = ?
                ''', (name,))
            
            return cursor.fetchone() is not None

    def get_all_products(self) -> List[Tuple]:
        """
        Получает все продукты из базы данных
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name
                FROM products 
                ORDER BY name
            ''')
            
            return cursor.fetchall()

    def update_product(self, product_id: int, name: str) -> bool:
        """
        Обновляет название продукта
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE products 
                SET name = ?
                WHERE id = ?
            ''', (name, product_id))
            
            conn.commit()
            return cursor.rowcount > 0

    def delete_product(self, product_id: int) -> bool:
        """
        Удаляет продукт по ID
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
            
            conn.commit()
            return cursor.rowcount > 0

    def get_products_count(self) -> int:
        """
        Возвращает общее количество продуктов в базе
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM products')
            return cursor.fetchone()[0]

    # === МЕТОДЫ ДЛЯ СВЯЗЕЙ ПРОДУКТОВ С ИНГРИДИЕНТАМИ И ПОЛУФАБРИКАТАМИ ===

    def add_ingredient_to_product(self, product_id: int, ingredient_id: int, quantity: float = 100) -> bool:
        """
        Добавляет ингридиент в продукт
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO products_ingredients (productId, ingredientId, quantity)
                    VALUES (?, ?, ?)
                ''', (product_id, ingredient_id, quantity))
                
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def add_semi_finished_to_product(self, product_id: int, semi_finished_id: int, quantity: float = 100) -> bool:
        """
        Добавляет полуфабрикат в продукт
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO products_semiFinished (productId, semiFinishedId, quantity)
                    VALUES (?, ?, ?)
                ''', (product_id, semi_finished_id, quantity))
                
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def remove_ingredient_from_product(self, product_id: int, ingredient_id: int) -> bool:
        """
        Удаляет ингридиент из продукта
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM products_ingredients 
                WHERE productId = ? AND ingredientId = ?
            ''', (product_id, ingredient_id))
            
            conn.commit()
            return cursor.rowcount > 0

    def remove_semi_finished_from_product(self, product_id: int, semi_finished_id: int) -> bool:
        """
        Удаляет полуфабрикат из продукта
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM products_semiFinished 
                WHERE productId = ? AND semiFinishedId = ?
            ''', (product_id, semi_finished_id))
            
            conn.commit()
            return cursor.rowcount > 0

    def get_product_ingredients(self, product_id: int) -> List[Dict]:
        """
        Получает все ингридиенты продукта с их количеством
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT i.id, i.name, i.calories, i.kJoule, i.proteins, i.fats, i.carbs, pi.quantity
                FROM products_ingredients pi
                JOIN ingredients i ON pi.ingredientId = i.id
                WHERE pi.productId = ?
                ORDER BY i.name
            ''', (product_id,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_product_semi_finished(self, product_id: int) -> List[Dict]:
        """
        Получает все полуфабрикаты продукта с их количеством
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT sf.id, sf.name, psf.quantity
                FROM products_semiFinished psf
                JOIN semiFinished sf ON psf.semiFinishedId = sf.id
                WHERE psf.productId = ?
                ORDER BY sf.name
            ''', (product_id,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def calculate_product_nutrition(self, product_id: int) -> Dict[str, float]:
        """
        Рассчитывает пищевую ценность продукта на 100г
        """
        ingredients = self.get_product_ingredients(product_id)
        
        semi_finished_list = self.get_product_semi_finished(product_id)
        
        if not ingredients and not semi_finished_list:
            return {'calories': 0, 'kJoule': 0, 'proteins': 0, 'fats': 0, 'carbs': 0}
        
        total_weight = 0
        total_calories = 0
        total_kJoule = 0
        total_proteins = 0
        total_fats = 0
        total_carbs = 0
        
        for ingredient in ingredients:
            factor = ingredient['quantity'] / 100.0
            total_weight += ingredient['quantity']
            total_calories += ingredient['calories'] * factor
            total_kJoule += ingredient['kJoule'] * factor
            total_proteins += ingredient['proteins'] * factor
            total_fats += ingredient['fats'] * factor
            total_carbs += ingredient['carbs'] * factor
        
        for sf in semi_finished_list:
            sf_nutrition = self.calculate_semi_finished_nutrition(sf['id'])
            factor = sf['quantity'] / 100.0
            total_weight += sf['quantity']
            total_calories += sf_nutrition['calories'] * factor
            total_kJoule += sf_nutrition['kJoule'] * factor
            total_proteins += sf_nutrition['proteins'] * factor
            total_fats += sf_nutrition['fats'] * factor
            total_carbs += sf_nutrition['carbs'] * factor
        
        if total_weight == 0:
            return {'calories': 0, 'kJoule': 0, 'proteins': 0, 'fats': 0, 'carbs': 0}
        
        factor_to_100g = 100.0 / total_weight
        
        return {
            'calories': round(total_calories * factor_to_100g, 2),
            'kJoule': round(total_kJoule * factor_to_100g, 2),
            'proteins': round(total_proteins * factor_to_100g, 2),
            'fats': round(total_fats * factor_to_100g, 2),
            'carbs': round(total_carbs * factor_to_100g, 2)
        }



db = IngredientDB()