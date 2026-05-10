import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from pathlib import Path

# Импортируем ваши модули
from model.model import ScrappingModuleModel
from view.view import ScrappingModuleView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowIcon(QIcon("view/icon.png"))
        #Создание главного окна
        self.setWindowTitle("Парсер соревнований по плаванию")
        self.resize(800, 600)
        
        #создание модели с логикой парсинга
        self.model = ScrappingModuleModel()
        
        #Создание View (интерфейс) и передача туда Модели
        self.view = ScrappingModuleView(self.model)
        
        #Установка View как центральный виджет
        self.setCentralWidget(self.view)
        
        #Указываем на то, что программу надо удалить из памяти после закрытия окна
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

def main():
    """Точка входа в приложение"""
    
    #Создание приложение
    app = QApplication(sys.argv)
    
    
    #Создание главного окна
    window = MainWindow()
    
    #Вывод окна
    window.show()
    
    #Запуск главного цикл событий
    sys.exit(app.exec())

if __name__ == "__main__":
    main()