import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from desktop.windows.login_window import LoginWindow

def main():
    app = QApplication(sys.argv)
    stack = QStackedWidget()

    login_window = LoginWindow(stack)
    stack.addWidget(login_window)

    stack.setWindowTitle("Сервис ремонта техники")
    stack.resize(1024, 768)
    stack.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
