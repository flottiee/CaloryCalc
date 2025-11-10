import sqlite3
import os
from database import db

def create_test_data():
    """Создает тестовые данные в базе"""
    
    # Очищаем существующие данные (опционально)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Очистка таблиц (раскомментируй если нужно очистить старые данные)
    # cursor.execute('DELETE FROM products_semiFinished')
    # cursor.execute('DELETE FROM products_ingredients')
    # cursor.execute('DELETE FROM semiFinished_ingredients')
    # cursor.execute('DELETE FROM products')
    # cursor.execute('DELETE FROM semiFinished')
    # cursor.execute('DELETE FROM ingredients')
    
    conn.commit()
    conn.close()
    
    # Тестовые ингредиенты
    ingredients = [
        # name, calories, proteins, fats, carbs
        ("Мука пшеничная", 364, 10.3, 1.0, 76.1),
        ("Сахар", 398, 0.0, 0.0, 99.8),
        ("Яйцо куриное", 157, 12.7, 11.5, 0.7),
        ("Молоко 3.2%", 64, 3.2, 3.6, 4.8),
        ("Масло сливочное", 748, 0.5, 82.5, 0.8),
        ("Соль", 0, 0, 0, 0),
        ("Дрожжи сухие", 325, 40.0, 6.0, 35.0),
        ("Вода", 0, 0, 0, 0),
        ("Лук репчатый", 41, 1.4, 0.2, 9.1),
        ("Мясо говяжье", 187, 18.9, 12.4, 0.0),
        ("Морковь", 35, 1.3, 0.1, 7.2),
        ("Картофель", 77, 2.0, 0.4, 16.3),
        ("Томатная паста", 82, 4.3, 0.2, 16.7),
        ("Сметана 20%", 206, 2.5, 20.0, 3.4),
        ("Сыр твердый", 360, 26.0, 26.5, 3.5),
    ]
    
    print("Добавляем ингредиенты...")
    ingredient_ids = {}
    for name, calories, proteins, fats, carbs in ingredients:
        try:
            ingredient_id = db.add_ingredient(name, calories, proteins, fats, carbs)
            ingredient_ids[name] = ingredient_id
            print(f"  - {name} (ID: {ingredient_id})")
        except Exception as e:
            print(f"Ошибка при добавлении {name}: {e}")
    
    # Тестовые полуфабрикаты
    print("\nДобавляем полуфабрикаты...")
    semi_finished = [
        "Тесто дрожжевое",
        "Фарш мясной", 
        "Овощная смесь",
        "Соус томатный"
    ]
    
    sf_ids = {}
    for name in semi_finished:
        try:
            sf_id = db.add_semi_finished(name)
            sf_ids[name] = sf_id
            print(f"  - {name} (ID: {sf_id})")
        except Exception as e:
            print(f"Ошибка при добавлении {name}: {e}")
    
    # Составы полуфабрикатов
    print("\nДобавляем составы полуфабрикатов...")
    
    # Тесто дрожжевое
    dough_composition = [
        ("Мука пшеничная", 500),
        ("Вода", 300),
        ("Дрожжи сухие", 10),
        ("Сахар", 20),
        ("Соль", 5),
        ("Масло сливочное", 30)
    ]
    
    for ing_name, quantity in dough_composition:
        if ing_name in ingredient_ids:
            db.add_ingredient_to_semi_finished(sf_ids["Тесто дрожжевое"], ingredient_ids[ing_name], quantity)
            print(f"  - Тесто дрожжевое: {ing_name} - {quantity}г")
    
    # Фарш мясной
    mince_composition = [
        ("Мясо говяжье", 800),
        ("Лук репчатый", 200),
        ("Соль", 10)
    ]
    
    for ing_name, quantity in mince_composition:
        if ing_name in ingredient_ids:
            db.add_ingredient_to_semi_finished(sf_ids["Фарш мясной"], ingredient_ids[ing_name], quantity)
            print(f"  - Фарш мясной: {ing_name} - {quantity}г")
    
    # Овощная смесь
    vegetables_composition = [
        ("Лук репчатый", 300),
        ("Морковь", 400),
        ("Картофель", 300)
    ]
    
    for ing_name, quantity in vegetables_composition:
        if ing_name in ingredient_ids:
            db.add_ingredient_to_semi_finished(sf_ids["Овощная смесь"], ingredient_ids[ing_name], quantity)
            print(f"  - Овощная смесь: {ing_name} - {quantity}г")
    
    # Соус томатный
    sauce_composition = [
        ("Томатная паста", 200),
        ("Вода", 300),
        ("Сметана 20%", 100),
        ("Соль", 5)
    ]
    
    for ing_name, quantity in sauce_composition:
        if ing_name in ingredient_ids:
            db.add_ingredient_to_semi_finished(sf_ids["Соус томатный"], ingredient_ids[ing_name], quantity)
            print(f"  - Соус томатный: {ing_name} - {quantity}г")
    
    # Тестовые продукты
    print("\nДобавляем продукты...")
    products = [
        "Пирожок с мясом",
        "Суп овощной",
        "Запеканка картофельная"
    ]
    
    product_ids = {}
    for name in products:
        try:
            product_id = db.add_product(name)
            product_ids[name] = product_id
            print(f"  - {name} (ID: {product_id})")
        except Exception as e:
            print(f"Ошибка при добавлении {name}: {e}")
    
    # Составы продуктов
    print("\nДобавляем составы продуктов...")
    
    # Пирожок с мясом
    pie_composition_ingredients = [
        ("Яйцо куриное", 50)
    ]
    
    for ing_name, quantity in pie_composition_ingredients:
        if ing_name in ingredient_ids:
            db.add_ingredient_to_product(product_ids["Пирожок с мясом"], ingredient_ids[ing_name], quantity)
            print(f"  - Пирожок с мясом (ингредиент): {ing_name} - {quantity}г")
    
    pie_composition_sf = [
        ("Тесто дрожжевое", 150),
        ("Фарш мясной", 100)
    ]
    
    for sf_name, quantity in pie_composition_sf:
        if sf_name in sf_ids:
            db.add_semi_finished_to_product(product_ids["Пирожок с мясом"], sf_ids[sf_name], quantity)
            print(f"  - Пирожок с мясом (полуфабрикат): {sf_name} - {quantity}г")
    
    # Суп овощной
    soup_composition_ingredients = [
        ("Вода", 500),
        ("Соль", 5),
        ("Сметана 20%", 50)
    ]
    
    for ing_name, quantity in soup_composition_ingredients:
        if ing_name in ingredient_ids:
            db.add_ingredient_to_product(product_ids["Суп овощной"], ingredient_ids[ing_name], quantity)
            print(f"  - Суп овощной (ингредиент): {ing_name} - {quantity}г")
    
    soup_composition_sf = [
        ("Овощная смесь", 300),
        ("Соус томатный", 200)
    ]
    
    for sf_name, quantity in soup_composition_sf:
        if sf_name in sf_ids:
            db.add_semi_finished_to_product(product_ids["Суп овощной"], sf_ids[sf_name], quantity)
            print(f"  - Суп овощной (полуфабрикат): {sf_name} - {quantity}г")
    
    # Запеканка картофельная
    casserole_composition_ingredients = [
        ("Сыр твердый", 100),
        ("Сметана 20%", 100),
        ("Соль", 5),
        ("Масло сливочное", 20)
    ]
    
    for ing_name, quantity in casserole_composition_ingredients:
        if ing_name in ingredient_ids:
            db.add_ingredient_to_product(product_ids["Запеканка картофельная"], ingredient_ids[ing_name], quantity)
            print(f"  - Запеканка картофельная (ингредиент): {ing_name} - {quantity}г")
    
    casserole_composition_sf = [
        ("Овощная смесь", 500)
    ]
    
    for sf_name, quantity in casserole_composition_sf:
        if sf_name in sf_ids:
            db.add_semi_finished_to_product(product_ids["Запеканка картофельная"], sf_ids[sf_name], quantity)
            print(f"  - Запеканка картофельная (полуфабрикат): {sf_name} - {quantity}г")
    
    print("\n" + "="*50)
    print("Тестовые данные успешно созданы!")
    print("="*50)
    
    # Показываем итоговую статистику
    print(f"\nИтоговая статистика:")
    print(f"Ингредиентов: {db.get_ingredients_count()}")
    print(f"Полуфабрикатов: {db.get_semi_finished_count()}")
    print(f"Продуктов: {db.get_products_count()}")
    
    # Показываем КБЖУ для продуктов
    print(f"\nКБЖУ продуктов:")
    for product_name, product_id in product_ids.items():
        nutrition = db.calculate_product_nutrition(product_id)
        print(f"  - {product_name}: К:{nutrition['calories']} Б:{nutrition['proteins']} Ж:{nutrition['fats']} У:{nutrition['carbs']}")

if __name__ == "__main__":
    create_test_data()