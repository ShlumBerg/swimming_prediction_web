from PyQt6.QtWidgets import QWidget, QFileDialog, QMessageBox
from PyQt6 import uic
from pathlib import Path
import os,subprocess
from sys import platform
from html import escape

class ScrappingModuleView(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model      #model из файла model.py
        self.folder=""          #Папка куда сохраняем файлы
        
        #Загрузка элементов интерфейса
        uic.loadUi("view/scrappingModule.ui", self)
        
        #Подключение сигналов из model
        self._connect_model_signals()
        
        #Подключаем действия пользователя
        self._connect_user_actions()
        
    def _connect_model_signals(self):
        '''Подключаем сигналы от модели '''
        self.model.status_signal.connect(self._on_model_status)
        
        self.model.error_signal.connect(self._on_model_error)
        
        self.model.finished_signal.connect(self._on_model_finished)
    
    def _connect_user_actions(self):
        '''Подключаем обработчики событий для действий пользователя'''
        self.btn_open_folder.clicked.connect(self._on_open_folder_clicked)
        self.btn_cancel.clicked.connect(self._on_cancel_clicked)
        self.btn_choose_folder.clicked.connect(self._on_choose_folder_clicked)
        self.btn_start.clicked.connect(self._on_start_clicked)
    
    def _on_choose_folder_clicked(self):
        '''При выборе папки'''
        folder=QFileDialog.getExistingDirectory(self,"Выберите папку для сохранения в неё данных:","")
        if folder:
            self.input_folder.setText(folder)
            self.log_browser.append("Папка выбрана: "+folder)
            self.folder=folder
            
            #Включаем элементы интерфейса
            self.btn_start.setEnabled(True)
            self.btn_open_folder.setEnabled(True)
    
    def _on_open_folder_clicked(self):
        '''Открыть папку в проводнике'''
        folder=self.folder
        if folder and Path(folder).exists():
            if platform=="win32":
                os.startfile(folder)  # Windows
            elif platform=="darwin":
                subprocess.Popen(['open',folder]) #Mac
            else:
                subprocess.Popen(['xdg-open',folder])  #Linux
        else:
            QMessageBox.warning(self, "Ошибка", "Выбранная папка перестала существовать!")
    
    def _on_cancel_clicked(self):
        '''Отменить текущий парсинг'''
        self.log_browser.append("Парсинг отменён!")
        
        self.model.cancel_scrapping()
        
        #Включаем объекты для папки сохранения и кнопку начала
        self.btn_choose_folder.setEnabled(True)
        self.folder_select_label.setEnabled(True)
        self.btn_start.setEnabled(True)
        
        #Выключаем надпись со сведениями о загрузке и кнопку "отмена"
        self.log_browser_label.setEnabled(False)
        self.btn_cancel.setEnabled(False)
        pass
    
    def _on_start_clicked(self):
        '''Начать парсинг'''
        #Проверяем, доступна ли папка
        if not self.folder or not Path(self.folder).exists():
            QMessageBox.warning(self, "Ошибка", "Выбранная папка перестала существовать!")
            return
        
        
        #Очищаем логи
        self.log_browser.clear()
        self.log_browser.append("Парсинг запущен!")
        
        
        self.model.start_scrapping(self.folder)
        
        #Выключаем объекты для папки сохранения и кнопку начала
        self.btn_choose_folder.setEnabled(False)
        self.folder_select_label.setEnabled(False)
        self.btn_start.setEnabled(False)
        
        #Включаем надпись со сведениями о загрузке и кнопку "отмена"
        
        self.log_browser_label.setEnabled(True)
        self.btn_cancel.setEnabled(True)
        pass
    
    def _on_model_status(self,message:str):
        '''При получении сообщения от model'''
        self.log_browser.append(message)
        
        #Прокрутить вниз
        scrollbar = self.log_browser.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def _on_model_error(self,message:str):
        '''При получении ошибки от model'''
        self.log_browser.append(f"<span style='color: red;'>{escape(message)}</span>")
        
        #Прокрутить вниз
        scrollbar = self.log_browser.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def _on_model_finished(self,is_success:bool):
        '''При завершении работы model'''
        if is_success:
            self.log_browser.append("Парсинг был завершён.")
        else:
            self.log_browser.append("Парсинг был остановлен.")
        #Включаем объекты для папки сохранения и кнопку начала
        self.btn_choose_folder.setEnabled(True)
        self.folder_select_label.setEnabled(True)
        self.btn_start.setEnabled(True)
        
        #Включаем надпись со сведениями о загрузке и кнопку "отмена"
        self.log_browser_label.setEnabled(False)
        self.btn_cancel.setEnabled(False)