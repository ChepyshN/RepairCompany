import PyQt6.QtWidgets
from PyQt6.QtGui import QAction

from desktop.windows.widgets import (
    DevicesManagerWidget, OrdersManagerWidget,
    WorksManagerWidget, WorkersWidget, OrdersWidget, WorksWidget, ClientsWidget, DevicesWidget, WorkerProfileWidget,
    ClientProfileWidget
)


class MainWindow(PyQt6.QtWidgets.QMainWindow):
    def __init__(self, stacked_widget, user):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.user = user
        self.profile_widget = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Главное окно - Сервис ремонта техники")

        # Центральный виджет и основной лейаут
        central_widget = PyQt6.QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = PyQt6.QtWidgets.QVBoxLayout()
        central_widget.setLayout(layout)

        # Приветствие
        greeting = PyQt6.QtWidgets.QLabel(f"Добро пожаловать, {self.user.get('name', 'Гость')}! Роль: {self.user.get('role', '')}")
        layout.addWidget(greeting)

        menubar = self.menuBar()
        profile_action = QAction("Мой профиль", self)
        profile_action.triggered.connect(self.open_profile)
        menubar.addAction(profile_action)

        self.menu_list = PyQt6.QtWidgets.QListWidget()
        layout.addWidget(self.menu_list)

        self.pages_stack = PyQt6.QtWidgets.QStackedWidget()
        layout.addWidget(self.pages_stack)

        if self.user.get('role') == 'client':
            self.pages = {
                'Устройства': DevicesManagerWidget(self.user),
                'Сотрудники': WorkersWidget(),
                'Заказы': OrdersWidget(self.user),
                'Работы': WorksWidget(self.user)
            }
        else:
            self.pages = {
                'Клиенты': ClientsWidget(),
                'Устройства': DevicesWidget(),
                'Заказы': OrdersManagerWidget(self.user),
                'Работы': WorksManagerWidget(self.user)
            }

        for page_name, widget in self.pages.items():
            self.menu_list.addItem(page_name)
            self.pages_stack.addWidget(widget)

        self.menu_list.currentRowChanged.connect(self.pages_stack.setCurrentIndex)
        self.menu_list.setCurrentRow(0)

        logout_btn = PyQt6.QtWidgets.QPushButton("Выход")
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)

    def open_profile(self):
        role = self.user.get('role')
        user_phone = self.user.get('phone')
        if not user_phone:
            PyQt6.QtWidgets.QMessageBox.warning(self, "Ошибка", "Не известен номер пользователя")
            return

        if role == 'worker':
            self.profile_widget = WorkerProfileWidget(user_phone)
        elif role == 'client':
            self.profile_widget = ClientProfileWidget(user_phone)
        else:
            PyQt6.QtWidgets.QMessageBox.information(self, "Информация", "Профиль для вашей роли не реализован")
            return

        self.profile_widget.show()

    def logout(self):
        self.stacked_widget.setCurrentIndex(0)
        self.stacked_widget.removeWidget(self)
        self.deleteLater()
