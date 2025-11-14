import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from widgets.calculator_tab import CalculatorTab
from widgets.ingredients_tab import IngredientsTab
from widgets.semi_finished_tab import SemiFinishedTab
from widgets.products_tab import ProductsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор калорий")
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
        self.tab_widget.addTab(self.ingredients_tab, "Ингредиенты")
        self.tab_widget.addTab(self.semi_finished_tab, "Полуфабрикаты")
        self.tab_widget.addTab(self.products_tab, "Продукты")
        
        layout.addWidget(self.tab_widget)

        self.tab_widget.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        """
        обработчик смены вкладки
        index - индекс активной вкладки
        """
        tab_name = self.tab_widget.tabText(index)

        #if index == 0 and tab_name == "Калькулятор":
        #    self.calculator_tab.on_tab_activated()
        #elif index == 1 and tab_name == "Ингридиенты":
        #    self.ingredients_tab.on_tab_activated()
        if index == 2 and tab_name == "Полуфабрикаты":
            self.semi_finished_tab.on_tab_activated()
        elif index == 3 and tab_name == "Продукты":
            self.products_tab.on_tab_activated()
            

def main():
    app = QApplication(sys.argv)
    

    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()