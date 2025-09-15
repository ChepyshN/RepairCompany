import hashlib
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QLabel, QComboBox
)
from PyQt6.QtCore import Qt
from app.business import register_user, get_user_by_phone
from app.helpers import validate_password, validate_phone


class LoginWindow(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Вход / Регистрация")
        self.resize(400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Войти", "Регистрация"])
        self.mode_selector.currentTextChanged.connect(self.switch_mode)
        self.layout.addWidget(self.mode_selector)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.name_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["client", "worker"])

        self.form_layout.addRow("Имя:", self.name_edit)
        self.form_layout.addRow("Телефон:", self.phone_edit)
        self.form_layout.addRow("Пароль:", self.password_edit)
        self.form_layout.addRow("Роль:", self.role_combo)

        self.submit_btn = QPushButton("Войти")
        self.submit_btn.clicked.connect(self.on_submit)
        self.layout.addWidget(self.submit_btn)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.status_label)

        self.switch_mode("Войти")

    def switch_mode(self, mode):
        if mode == "Войти":
            self.name_edit.setVisible(False)
            self.role_combo.setVisible(False)
            self.submit_btn.setText("Войти")
            self.status_label.clear()
        else:
            self.name_edit.setVisible(True)
            self.role_combo.setVisible(True)
            self.submit_btn.setText("Зарегистрироваться")
            self.status_label.clear()

    def on_submit(self):
        mode = self.mode_selector.currentText()
        name = self.name_edit.text().strip()
        if validate_phone(self.phone_edit.text().strip()) : phone = self.phone_edit.text().strip()
        else:
            self.status_label.setText("Неправильный формат телефона")
            phone = None
        if validate_password(self.password_edit.text()) : password = self.password_edit.text()
        else:
            self.status_label.setText("Неправильный формат пароля (минимум 4 символа)")
            password = None
        role = self.role_combo.currentText()

        if not phone or not password or (mode == "Регистрация" and not name):
            self.status_label.setText("Убедитесь, что формат телефона и пароля правильный (минимум 4 символа)")
            return

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if mode == "Регистрация":
            try:
                existing_user = get_user_by_phone(phone)
                if existing_user:
                    self.status_label.setText("Пользователь с таким телефоном уже существует.")
                    return

                res = register_user(name, phone, password_hash, role)
                if res and len(res) > 0:
                    self.status_label.setText(f"Пользователь {name} зарегистрирован как {role}.")
                    self.mode_selector.setCurrentText("Войти")
                else:
                    self.status_label.setText("Ошибка при регистрации.")
            except Exception as e:
                self.status_label.setText(f"Ошибка при регистрации: {str(e)}")
        else:
            user = get_user_by_phone(phone)
            if not user:
                self.status_label.setText("Пользователь не найден.")
                return
            if user.get("password_hash") != password_hash:
                self.status_label.setText("Неверный пароль.")
                return

            self.status_label.setText(f"Добро пожаловать, {user['name']}!")
            from desktop.windows.main_window import MainWindow
            main_window = MainWindow(self.stacked_widget, user)
            self.stacked_widget.addWidget(main_window)
            self.stacked_widget.setCurrentWidget(main_window)
