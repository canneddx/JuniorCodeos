import subprocess
import psutil
import webbrowser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, 
                             QHBoxLayout, QDialog, QListWidget, QFileDialog, QComboBox, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, pyqtProperty
from PyQt5.QtGui import QPixmap, QColor, QPainter, QBrush, QFont
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QGraphicsBlurEffect
import os
from PyQt5 import QtWidgets
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
import sys

class HoverLabel(QWidget):
    def __init__(self, icon_path=None, url=None, parent=None):
        super().__init__(parent)
        self._hover_opacity = 0
        self.icon_path = icon_path
        self.url = url  # URL for the icon click

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(1)

        if self.icon_path:
            self.icon_label = QLabel(self)
            self.icon_label.setPixmap(QPixmap(self.icon_path).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)

        self.setStyleSheet("""
            QWidget {
                padding: 10px;
                border-radius: 10px;
                background-color: transparent;
            }
        """)
        self.hover_animation = QPropertyAnimation(self, b"hoverOpacity")
        self.hover_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.hover_animation.setDuration(300)
        self.setMouseTracking(True)


    def getHoverOpacity(self):
        return self._hover_opacity

    def setHoverOpacity(self, opacity):
        self._hover_opacity = opacity
        self.update()

    hoverOpacity = pyqtProperty(float, getHoverOpacity, setHoverOpacity)

    def enterEvent(self, event):
        self.hover_animation.setStartValue(self._hover_opacity)
        self.hover_animation.setEndValue(0.1)
        self.hover_animation.start()

    def leaveEvent(self, event):
        self.hover_animation.setStartValue(self._hover_opacity)
        self.hover_animation.setEndValue(0.0)
        self.hover_animation.start()

    def mousePressEvent(self, event):
        if self.url:
            webbrowser.open(self.url)  # Open the URL when clicked

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = QColor(0, 0, 0, int(self._hover_opacity * 255))
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)
        super().paintEvent(event)


class ToggleButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._color = QColor(173, 216, 230)  # Light blue color initially
        self.setStyleSheet(f"background-color: {self._color.name()}; border-radius: 35px; font-size: 16px; color: white;")
        self.setFixedSize(150, 70)
        self.setText("OFF")
        self.clicked.connect(self.on_click)

        # Добавление тени
        self.shadow_effect = QGraphicsDropShadowEffect(self)
        self.shadow_effect.setBlurRadius(20)  # Радиус размытия
        self.shadow_effect.setOffset(0, 5)  # Смещение тени
        self.shadow_effect.setColor(QColor(0, 0, 0, 120))  # Цвет тени с прозрачностью
        self.setGraphicsEffect(self.shadow_effect)

        self._text_opacity = 1.0  # Initial text opacity for animation

        self.anim = QPropertyAnimation(self, b"color")
        self.anim.setDuration(500)  # Animation duration
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)

        self.text_anim = QPropertyAnimation(self, b"textOpacity")
        self.text_anim.setDuration(500)  # Text animation duration
        self.text_anim.setEasingCurve(QEasingCurve.InOutQuad)

    def getColor(self):
        return self._color

    def setColor(self, color):
        self._color = color
        self.setStyleSheet(f"background-color: {self._color.name()}; border-radius: 35px; font-size: 16px; color: white;")

    color = pyqtProperty(QColor, getColor, setColor)

    def getTextOpacity(self):
        return self._text_opacity

    def setTextOpacity(self, opacity):
        self._text_opacity = opacity
        self.update()

    textOpacity = pyqtProperty(float, getTextOpacity, setTextOpacity)

    def on_click(self):
        if self._color == QColor(173, 216, 230):  # Light blue
            self.anim.setStartValue(self._color)
            self.anim.setEndValue(QColor(144, 238, 144))  # Light green
            self.text_anim.setStartValue(self._text_opacity)
            self.text_anim.setEndValue(0.0)  # Fade out text
            self.setText("ON")
            self.run_program()  # Run the program when it's "ON"
        else:
            self.anim.setStartValue(self._color)
            self.anim.setEndValue(QColor(173, 216, 230))  # Light blue
            self.text_anim.setStartValue(self._text_opacity)
            self.text_anim.setEndValue(1.0)  # Fade in text
            self.setText("OFF")
            self.stop_program()  # Stop the program when it's "OFF"

        self.anim.start()
        self.text_anim.start()

    def reset(self):
        self.setText("OFF")
        self.setColor(QColor(173, 216, 230))  # Reset to light blue

    def run_program(self):
        # Check which program to run based on the button's state
        if self.text() == "ON":
            program_title = self.parent().title_label.text().strip()  # Optional: strip any extra spaces
            print(f"Program title: {program_title}")  # Debugging line

            # Match program titles to their corresponding batch or executable files
            if program_title.lower() == "youtube":
                print("Running Youtube...")  # Debugging line
                subprocess.Popen(["youtube.exe"], shell=True)
            elif program_title.lower() == "youtube + discord":
                print("Running Youtube + Discord...")  # Debugging line
                subprocess.Popen(["mods\youtube_discord.exe"], shell=True)  # Use double backslashes for file paths
            elif program_title.lower() == "discord":
                print("Running Discord...")  # Debugging line
                subprocess.Popen(["mods\\discord.bat"], shell=True)  # Run discord.bat
            else:
                print(f"Ошибка: неизвестное название программы! (Received title: {program_title})")

    def stop_winws(self):
        for proc in psutil.process_iter():
            try:
                if proc.name() == "winws.exe":
                    proc.terminate()
                    print("winws.exe closed.")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def stop_win_divert(self):
        for proc in psutil.process_iter():
            try:
                if proc.name() in ["WinDivert64.sys", "WinDivert.dll"]:
                    proc.terminate()
                    print(f"{proc.name()} closed.")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def stop_program(self):
        self.stop_winws()  # Остановить winws.exe

    def closeEvent(self, event):
        self.stop_winws()  # Остановить winws.exe
        self.stop_win_divert()  # Остановить WinDivert
        event.accept()
    

class SettingsButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333;
                border: 2px solid #ccc;
                border-radius: 10px;
                font-size: 16px;
                padding: 10px 20px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border-color: #888;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
                border-color: #555;
            }
        """)
        self.setCursor(Qt.PointingHandCursor)  # Указатель в виде руки при наведении

        # Добавление тени
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 160))  # Полупрозрачный черный цвет
        self.setGraphicsEffect(shadow)

class ModsDialog(QDialog):
    def __init__(self, parent, mods_folder):
        # Используем путь к папке mods в той же директории, где находится скрипт
        mods_folder = os.path.join(os.path.dirname(sys.executable), 'mods') if getattr(sys, 'frozen', False) else os.path.join(os.path.dirname(__file__), 'mods')
        super().__init__(parent)
        self.setWindowTitle("Моды")
        self.setFixedSize(400, 300)
        self.mods_folder = mods_folder

        self.layout = QVBoxLayout(self)

        # Создаем список модов
        self.mods_list = QListWidget(self)
        self.layout.addWidget(self.mods_list)

        # Заполняем список модов из папки модов
        if os.path.exists(self.mods_folder):
            for mod in os.listdir(self.mods_folder):
                if mod.endswith('.bat'):  # Предполагаем, что моды - это .bat файлы
                    self.mods_list.addItem(mod)
        else:
            print(f"Папка {self.mods_folder} не существует.")

        # Добавляем обработчик двойного клика
        self.mods_list.itemDoubleClicked.connect(self.run_mod)

        # Добавляем гиперссылку для открытия папки модов
        self.link_label = QLabel('<a href="mods">Не нашли свои моды?</a>', self)
        self.link_label.setOpenExternalLinks(True)
        self.layout.addWidget(self.link_label)

    def run_mod(self, item):
        mod_name = item.text()  # Получаем имя файла мода
        mod_path = os.path.join(self.mods_folder, mod_name)  # Полный путь к моду

        try:
            subprocess.Popen([mod_path], shell=True)  # Запускаем мод
        except Exception as e:
            print(f"Ошибка при запуске мода {mod_name}: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JuniorCodeos")
        self.setWindowIcon(QIcon("photo\JCC.ico"))
        self.setFixedSize(450, 460)

        # Путь до папки 'mods' в той же директории
        self.mods_folder = os.path.join(os.getcwd(), 'mods')
        os.makedirs(self.mods_folder, exist_ok=True)  # Создаем папку mods, если её нет
        
        # Добавляем кнопку для открытия модов
        button2 = QPushButton("Моды", self)
        button2.clicked.connect(lambda: self.open_mods())  # Открываем диалог с папкой mods
        self.setCentralWidget(button2)

        self.background_label = QLabel(self)
        pixmap = QPixmap("photo/main.jpg")
        self.background_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        # Apply blur effect
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(5)
        self.background_label.setGraphicsEffect(blur_effect)

        # Title label with bold text and dark outline
        self.title_label = QLabel("JuniorCodeos", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-weight: bold;
            font-size: 22px;
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        """)
        
        self.title_label.setGeometry(0, 20, self.width(), 50)

        # Update label with bold text and dark outline
        self.update_label = QLabel("Следите за обновлениями", self)
        self.update_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.update_label.setStyleSheet("""
            font-size: 18px;
            color: #333;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        """)
        self.update_label.setFixedSize(self.width(), 30)
        self.update_label.move(0, 300)

        # Layout for the settings buttons
        self.settings_button_layout = QVBoxLayout()
        self.settings_button_layout.setSpacing(9)
        self.settings_button_layout.setAlignment(Qt.AlignCenter)

        button1 = SettingsButton("Оптимизация", self)
        button1.clicked.connect(self.run_optimization)
        button2 = SettingsButton("Моды", self)
        button2.clicked.connect(self.open_mods)
        button3 = SettingsButton("tap-to-control", self)
        button3.clicked.connect(self.open_tap)
        button4 = SettingsButton("Обновления", self)
        button4.clicked.connect(self.open_obl)

        # Add buttons to the layout
        self.settings_button_layout.addWidget(button1)
        self.settings_button_layout.addWidget(button2)
        self.settings_button_layout.addWidget(button3)
        self.settings_button_layout.addWidget(button4)

        # Create a widget for the buttons and place it in the main window
        self.settings_buttons_widget = QWidget(self)
        self.settings_buttons_widget.setLayout(self.settings_button_layout)
        self.settings_buttons_widget.setFixedSize(300, 200)

        # Center the buttons widget vertically
        self.settings_buttons_widget.move(
            (self.width() - self.settings_buttons_widget.width()) // 2,
            (self.height() - self.settings_buttons_widget.height()) // 2 - 30
        )

        # Icons for Telegram and VK (Example for icon layout)
        self.icon_layout = QVBoxLayout()
        self.icon_layout.setSpacing(60)
        self.icon_layout.setAlignment(Qt.AlignCenter)

        # Иконка Telegram
        self.icon_tg = HoverLabel(icon_path="photo/jc.png", url="https://hipolink.me/juniorcodeos", parent=self)
        self.icon_tg.icon_label.setPixmap(QPixmap(self.icon_tg.icon_path).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.icon_layout.addWidget(self.icon_tg)

        # Размещение иконок
        self.icons_widget = QWidget(self)
        self.icons_widget.setLayout(self.icon_layout)
        self.icons_widget.setFixedSize(200, 200)
        self.icons_widget.move((self.width() - self.icons_widget.width()) // 2, 110)

        # Отображение текста и иконок на вкладке JuniorCodeos
        self.update_label.setVisible(True)
        self.icons_widget.setVisible(True)

        # Боковое меню
        self.menu_widget = QWidget(self)
        self.menu_widget.setFixedSize(80, self.height())
        self.menu_widget.move(-80, 0)
        self.menu_widget.setStyleSheet("background-color: #F5F5F5; border-radius: 10px;")

        menu_layout = QVBoxLayout(self.menu_widget)
        menu_layout.setAlignment(Qt.AlignTop)

        self.support_label = QLabel(self)
        self.support_label.setAlignment(Qt.AlignCenter)
        self.support_label.setText('<a href="https://t.me/juniorcodeos">Поддержка</a>')
        self.support_label.setStyleSheet("""
            font-size: 14px;
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
            text-decoration: none;
        """)
        # Размещаем текст внизу окна
        self.support_label.setGeometry(0, self.height() - 30, self.width(), 30)
        self.support_label.setOpenExternalLinks(True)  # Включаем возможность открывать ссылку по клику

        # Обработчик клика на ссылку
        self.support_label.linkActivated.connect(self.open_support_link)

        # Вкладка "Youtube"
        self.menu_label = HoverLabel(icon_path="photo/youtube.png", parent=self)
        self.menu_label.mousePressEvent = self.set_title_youtube
        menu_layout.addWidget(self.menu_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("margin: 5px 0; color: #ccc;")
        menu_layout.addWidget(separator)

        # Вкладка "Youtube + Discord"
        self.menu_label2 = HoverLabel(icon_path="photo/discord.png", parent=self)
        self.menu_label2.mousePressEvent = self.set_title_youtube_discord
        menu_layout.addWidget(self.menu_label2)

        # Вкладка "Youtube + Discord"
        self.menu_label3 = HoverLabel(icon_path="photo/YD.png", parent=self)
        self.menu_label3.mousePressEvent = self.set_title_chatgpt
        menu_layout.addWidget(self.menu_label3)

        # Spacer для растягивания элементов вверх и закрепления иконки внизу
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        menu_layout.addItem(spacer)

        # Вкладка "Настройки" (иконка gear)
        self.menu_label4 = HoverLabel(icon_path="photo/gear.png", parent=self)
        self.menu_label4.mousePressEvent = self.set_title_settings
        menu_layout.addWidget(self.menu_label4)

        # Кнопка ToggleButton скрыта по умолчанию для JuniorCodeos
        self.toggle_button = ToggleButton(self)
        self.toggle_button.move((self.width() - self.toggle_button.width()) // 2, (self.height() - self.toggle_button.height()) // 2)
        self.toggle_button.setVisible(False)
        self.settings_buttons_widget.setVisible(False)

        # Кнопка "Гамбургер" для бокового меню
        self.hamburger_button = QPushButton("☰", self)
        self.hamburger_button.setFixedSize(40, 40)
        self.hamburger_button.setStyleSheet("background-color: transparent; border: none; font-size: 20px; padding-left: 5px;")
        self.hamburger_button.clicked.connect(self.toggle_menu)

        self.animation = QPropertyAnimation(self.menu_widget, b"pos")
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.setDuration(450)
        self.animation.valueChanged.connect(self.update_button_position)

        self.menu_open = False
        self.update_button_position()

        self.animation = QPropertyAnimation(self.menu_widget, b"pos")
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.setDuration(450)
        self.animation.valueChanged.connect(self.update_button_position)

        self.menu_open = False
        self.update_button_position()

        self.animation = QPropertyAnimation(self.menu_widget, b"pos")
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.setDuration(410)
        self.animation.valueChanged.connect(self.update_button_position)

        self.menu_open = False
        self.update_button_position()

    def open_support_link(self):
        # Метод для открытия ссылки в браузере (можно использовать, например, QDesktopServices)
        QDesktopServices.openUrl(QUrl("https://hipolink.me/juniorcodeos"))

    def toggle_menu(self):
        end_pos = QPoint(0, 0) if not self.menu_open else QPoint(-90, 0)
        self.animation.setStartValue(self.menu_widget.pos())
        self.animation.setEndValue(end_pos)
        self.animation.start()
        self.menu_open = not self.menu_open

    def update_button_position(self):
        self.hamburger_button.move(self.menu_widget.x() + self.menu_widget.width(), 5)

    def show_toggle_button(self, show):
        self.toggle_button.setVisible(show)

    def apply_text_shadow(self, label):
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(-5, 3)  # Смещение тени влево по оси X и вниз по оси Y
        shadow.setBlurRadius(20)  # Радиус размытия тени
        shadow.setColor(Qt.black)  # Цвет тени
        label.setGraphicsEffect(shadow)

    def set_title_youtube(self, event):
        self.title_label.setText("YouTube")
        self.update_label.setVisible(False)
        self.icons_widget.setVisible(False)
        self.toggle_button.reset()
        self.show_toggle_button(True)
        self.toggle_menu()

        self.title_label.move(0, 80)
        self.settings_buttons_widget.setVisible(False)

        # Применяем жирный шрифт к кнопкам
        self.apply_bold_font_to_buttons()

        # Применяем тень к тексту
        self.apply_text_shadow(self.title_label)

    def set_title_youtube_discord(self, event):
        self.title_label.setText("Discord")
        self.update_label.setVisible(False)
        self.icons_widget.setVisible(False)
        self.toggle_button.reset()
        self.show_toggle_button(True)
        self.toggle_menu()

        self.title_label.move(0, 80)
        self.settings_buttons_widget.setVisible(False)

        # Применяем жирный шрифт к кнопкам
        self.apply_bold_font_to_buttons()

        # Применяем тень к тексту
        self.apply_text_shadow(self.title_label)

    def set_title_chatgpt(self, event):
        self.title_label.setText("Youtube + Discord")
        self.update_label.setVisible(False)
        self.icons_widget.setVisible(False)
        self.toggle_button.reset()
        self.show_toggle_button(True)
        self.toggle_menu()


        self.title_label.move(0, 80)
        self.settings_buttons_widget.setVisible(False)

        # Применяем жирный шрифт к кнопкам
        self.apply_bold_font_to_buttons()

        # Применяем тень к тексту
        self.apply_text_shadow(self.title_label)

    def set_title_settings(self, event):
        self.title_label.setText("Настройки")
        self.update_label.setVisible(False)
        self.icons_widget.setVisible(False)
        self.toggle_button.reset()
        self.show_toggle_button(False)  
        self.toggle_menu()

        self.title_label.move(0, 60)
        self.settings_buttons_widget.setVisible(True)

        self.apply_bold_font_to_buttons()

        self.apply_text_shadow(self.title_label)

    def apply_bold_font_to_buttons(self):
        for button in self.settings_buttons_widget.findChildren(QtWidgets.QPushButton):
            font = QFont()
            font.setBold(True)
        button.setFont(font)

    def run_optimization(self):
        """Runs the 'wan.bat' batch file through CMD."""
        try:
            subprocess.run(['cmd.exe', '/c', 'start', 'WAN\WAN.bat'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running the batch file: {e}")

    def open_mods(self):
        if not os.path.exists(self.mods_folder):
            os.makedirs(self.mods_folder)  # Create the folder if it doesn't exist
        os.startfile(self.mods_folder)

    def open_tap(self):
        try:
            subprocess.run(['tap-to-control.exe'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running the batch file: {e}")

    def init_ui(self):
        # Создаем кнопку "Моды" и подключаем её к обработчику
        mods_button = SettingsButton("Моды", self)
        mods_button.clicked.connect(self.open_mods)  # Подключение к обработчику
        self.settings_button_layout.addWidget(mods_button)

    def open_mods(self):
        # Открытие диалога с модами
        mods_folder = os.path.join(os.path.dirname(sys.executable), "mods")
        self.mods_dialog = ModsDialog(self, mods_folder)
        self.mods_dialog.exec_()  # Открытие модального диалога

    def open_obl(self):
        try:
            subprocess.run(['cmd.exe', '/c', 'start', 'update.bat'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

        

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


