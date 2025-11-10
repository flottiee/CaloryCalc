import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from widgets.calculator_tab import CalculatorTab
from widgets.ingredients_tab import IngredientsTab
from widgets.semi_finished_tab import SemiFinishedTab
from widgets.products_tab import ProductsTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление продуктами")
        self.setGeometry(100, 100, 800, 600)
        
        self._setup_ui()
    
    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        self.tab_widget = QTabWidget()
        
        self.calculator_tab = CalculatorTab()
        self.ingredients_tab = IngredientsTab()
        self.semi_finished_tab = SemiFinishedTab()
        self.products_tab = ProductsTab()
        
        self.tab_widget.addTab(self.calculator_tab, "Калькулятор")
        self.tab_widget.addTab(self.ingredients_tab, "Ингридиенты")
        self.tab_widget.addTab(self.semi_finished_tab, "Полуфабрикаты")
        self.tab_widget.addTab(self.products_tab, "Продукты")
        
        layout.addWidget(self.tab_widget)

def main():
    app = QApplication(sys.argv)
    
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()