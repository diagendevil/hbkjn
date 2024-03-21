import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QListWidgetItem
from ui import Ui_MainWindow

class Widget(QMainWindow):
    def   __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_data()

        #Підключення кнопок
        self.ui.pushButton.clicked.connect(self.add_note)
        self.ui.pushButton_3.clicked.connect(self.save_note)
        self.ui.pushButton_2.clicked.connect(self.del_note)
        self.ui.pushButton_4.clicked.connect(self.add_tag)
        self.ui.pushButton_5.clicked.connect(self.del_tag)
        self.ui.pushButton_6.clicked.connect(self.serch_by_tag)

        # Підключення події вибору елемента у списку заміток
        self.ui.listWidget.itemClicked.connect(self.show_note)

    def load_data(self):
        try:
            #Зчитування даних з файлу "notes_data.json"
            with open("notes_data.json","r", encoding='utf-8')as file:
                self.notes = json.load(file)
        except(FileNotFoundError, json.JSONDecodeError):
            #Обробка винятків, якщо файл відсутній або не вірний формат
            self.notes = {}
        #Додавання заміток до списку у графічному інтерфейсі
        self.ui.listWidget.addItems(self.notes.keys())

    def add_note(self):
        # QInputDialog.getText() відкртити вікно з полем для введення тексту та кнопками "Ок" та "Скасувати"
        note_name, ok = QInputDialog.getText(self, "Додати замітку", "Назва замітки:")
        # Перевірка чи користувач натиснув "Ок" і чи введено назву нашої замітки
        if ok and note_name != "":
            # Перевіримо, чи замітка вже існує
            if note_name not in self.notes:
                self.notes[note_name] = {"текст": "", "теги": []}
                # Оновимо список заміток у графічному інтерфейсі
                self.ui.listWidget.addItem(note_name)
            # Оновіть текст лише в разі його відсутності
            self.notes[note_name]["текст"] = self.ui.textEdit.toPlainText()
            # Оновимо список тегів
            self.ui.listWidget_2.clear()
            self.ui.listWidget_2.addItems(self.notes[note_name]["теги"])
            # Встановимо текст замітки як існуючий або оновлений текст
            self.ui.textEdit.setPlainText(self.notes[note_name]["текст"])
            print(self.notes)


    def show_note(self):
        # Перевірка, чи є обрані елементи в списку
        if self.ui.listWidget.selectedItems():
            # Отримання тексту обраної замітки зі списку
            key = self.ui.listWidget.selectedItems()[0].text()
            # Перевіримо, чи є текст у поточній замітці перед оновленням поля редагування
            if "текст" in self.notes[key]:
                # Встановлюємо текст замітки у поле для редагування (QTextEdit)
                self.ui.textEdit.setPlainText(self.notes[key]["текст"])
            else:
                # Якщо текст відсутній, очистимо поле для редагування
                self.ui.textEdit.clear()
            # Очищаємо список тегів
            self.ui.listWidget_2.clear()
            # Додаємо теги з обраної замітки до списку тегів у графічному інтерфейсі
            self.ui.listWidget_2.addItems(self.notes[key]["теги"])

    def save_note(self):
        # перевірити чи обрано замітку зі списку
        if self.ui.listWidget.selectedItems():
            # Отримуємо назву обраної замітки
            key = self.ui.listWidget.selectedItems()[0].text()
            # Збереження тексту замітки у словнику "notes"
            self.notes[key]["текст"] = self.ui.textEdit.toPlainText()
            # Оновимо список тегів у граф. інтерфейсі
            self.ui.listWidget_2.clear()
            self.ui.listWidget_2.addItems(self.notes[key]["теги"])
            # Оновимо список заміток у граф. інтерфейсі
            self.ui.listWidget.clear()
            self.ui.listWidget.addItems(self.notes.keys())
            # Запишемо увесь словник 'notes' у файл "notes_data.json"
            with open("notes_data.json", "w", encoding='utf-8') as file:
                json.dump(self.notes, file, sort_keys=True, ensure_ascii=False)
            print(self.notes)
        else:
            print("Замітка для збереження не вибрана!")


    def del_note(self):
        # Перевіримо чи обрано нашу замітку зі списку
        # selectedItems() - використовуємо для отримання списку обраних елементів
        # [0].text() - отримуємо вміст обраного елемента
        if self.ui.listWidget.selectedItems():
            # Отримуємо назву обраної замітки
            key = self.ui.listWidget.selectedItems()[0].text()
            # Вилучимо нашу замітку зі словника notes
            del self.notes[key]
            # Очистимо список тегів у граф. інтерфейсі
            self.ui.listWidget_2.clear()
            # Очистимо поле для редагування тексту
            self.ui.textEdit.clear()
            # Запишимо увесь словник 'notes' у файл "notes_data.json"
            with open("notes_data.json", "w", encoding='utf-8') as file:
                json.dump(self.notes, file, sort_keys=True, ensure_ascii=False)
            # Оновимо список заміток у граф. інтерфейсі після вилучення
            self.ui.listWidget.clear()
            self.ui.listWidget.addItems(self.notes.keys())
        else:
            print("Замітка для вилучення не вибрана!")
    
    def add_tag(self):
        # Перевіримо чи обрано замітку зі списку
        if self.ui.listWidget.selectedItems():
            # Отримання назави обраноії замітки
            key = self.ui.listWidget.selectedItems()[0].text()
            # отримаємо текст тегу з поля введення
            tag = self.ui.lineEdit.text()
            # Перевіримо чи відсутній в списку тегів обраної замітки
            if not tag in self.notes[key]["теги"]:
                # Додамо тег до списку тегів у словнику "notes"
                self.notes[key]["теги"].append(tag)
                # Видалимо теги у граф інтерф
                self.ui.listWidget_2.clear()
                # Додати тег до спику в граф. інтерфейсі
                self.ui.listWidget_2.addItems(self.notes[key]["теги"])
                # Очистимо поле для введення тегу
                self.ui.lineEdit.clear()
            # Запишемо оновлений словник notes у файл
            with open("notes_data.json","w", encoding ="utf-8") as file:
                json.dump(self.notes, file, sort_keys= True)
    
    def del_tag(self):
        #Перевіримо чи обраний тег у списку тегів
        if self.ui.listWidget_2.selectedItems():
            #Отримаємо назву обраної замітки
            # selectedItems() - використовуємо для отримання списку обраних елементів
            # [0].text() - отримуємо вміст обраного елемента
            key = self.ui.listWidget.selectedItems()[0].text()
            # Отримання тексту обраного тегу
            tag = self.ui.listWidget_2.selectedItems()[0].text()
            # Вилучимо тег зі списку тегів у словнику "notes"
            self.notes[key]["теги"].remove(tag)
            # Очистимо список тегів у граф.інтерфейсі
            self.ui.listWidget_2.clear()
            # Додамо залишені теги обраної замітки
            self.ui.listWidget_2.addItems(self.notes[key]["теги"])
            # Запишиме онолений словник у json файл
            with open("notes_data.json","w", encoding = "utf-8")as file:
                json.dump(self.notes, file, sort_keys= True)
        else:
            print("Тег для вилучення не обраний")
    
    def serch_by_tag(self):
        #перевиримо чи введено слово для пошуку
        tag, ok = QInputDialog.getText(self, "Пошук за тегом","Введіть тег")
        if ok and tag!="":
            #Очищення списку заміток та тексового поля
            self.ui.listWidget.clear()
            self.ui.textEdit.clear()
            # Пошук заміток, що містять введений тег
            matching_notes = [note for note, data in self.notes.items() if tag in data["теги"]]
            self.ui.listWidget.addItems(matching_notes)
        else:
            print("Помилка під час пошуку")

app = QApplication([])
ex = Widget()
ex.show()
app.exec_()
