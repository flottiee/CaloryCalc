from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class CalculatorTab(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Заглушка для содержимого вкладки "Калькулятор"
        label = QLabel("Содержимое вкладки 'Калькулятор'")
        label.setStyleSheet("font-size: 16px; padding: 20px;")
        layout.addWidget(label)