from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, \
    QPushButton, QComboBox, QInputDialog, QHBoxLayout
from app.business import list_devices, list_clients, list_orders, list_workers, list_works, list_specs, edit_worker, \
    edit_client, register_device, edit_device, remove_device, remove_order, register_order, edit_order, \
    remove_work, register_work, get_my_client, get_my_worker
from app.db import get_client_by_phone, get_worker_by_phone
from app.helpers import validate_email


class DevicesWidget(QWidget):
    def __init__(self, user=None):
        super().__init__()
        self.user = user
        self.all_devices = []
        self.init_ui()
        self.load_devices()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Устройства"))

        # Поисковая панель
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Поиск по типу устройства")
        self.search_btn = QPushButton("Поиск")
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(self.search_btn)
        layout.addLayout(search_layout)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.search_btn.clicked.connect(self.perform_search)

    def load_devices(self):
        if self.user and self.user.get('role') == 'client':
            self.all_devices = [d for d in list_devices() if d.get('client_id') == self.user['id']]
        else:
            self.all_devices = list_devices()
        self.show_devices(self.all_devices)

    def show_devices(self, devices):
        self.table.clear()
        self.table.setRowCount(len(devices))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Тип"])

        for row, device in enumerate(devices):
            self.table.setItem(row, 0, QTableWidgetItem(str(device.get("id", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(device.get("name", "")))
            self.table.setItem(row, 2, QTableWidgetItem(device.get("type", "")))

    def perform_search(self):
        query = self.search_edit.text().strip().lower()
        if not query:
            self.show_devices(self.all_devices)
            return

        filtered = [d for d in self.all_devices if query in (d.get("type") or "").lower()]
        self.show_devices(filtered)

class ClientsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        label = QLabel("Клиенты")
        layout.addWidget(label)

        table = QTableWidget()
        layout.addWidget(table)

        clients = list_clients()
        table.setRowCount(len(clients))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["ID", "Имя", "Телефон", "Email"])

        for row, client in enumerate(clients):
            table.setItem(row, 0, QTableWidgetItem(str(client.get("id", ""))))
            table.setItem(row, 1, QTableWidgetItem(client.get("name", "")))
            table.setItem(row, 2, QTableWidgetItem(client.get("phone", "")))
            table.setItem(row, 3, QTableWidgetItem(client.get("email", "")))

class OrdersWidget(QWidget):
    def __init__(self, user=None, worker=None):
        super().__init__()
        self.user = user
        self.worker = worker
        self.init_ui()

    def init_ui(self):
        client = get_my_client(self.user['phone'])
        layout = QVBoxLayout()
        self.setLayout(layout)
        label = QLabel("Заказы")
        layout.addWidget(label)

        table = QTableWidget()
        layout.addWidget(table)

        orders = list_orders()
        if self.user and self.user.get('role') == 'client':
            device_ids = [d['id'] for d in list_devices() if d.get('client_id') == client.get('id')]
            orders = [o for o in orders if o.get('client_id') == client.get('id') or o.get('device_id') in device_ids]
        elif self.worker:
            orders = [o for o in orders]

        table.setRowCount(len(orders))
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["ID", "Статус", "Клиент ID", "Устройство ID", "Описание"])

        for row, order in enumerate(orders):
            table.setItem(row, 0, QTableWidgetItem(str(order.get("id", ""))))
            table.setItem(row, 1, QTableWidgetItem(order.get("status", "")))
            table.setItem(row, 2, QTableWidgetItem(str(order.get("client_id", ""))))
            table.setItem(row, 3, QTableWidgetItem(str(order.get("device_id", ""))))
            table.setItem(row, 4, QTableWidgetItem(order.get("description", "")))

class WorkersWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.all_workers = []
        self.init_ui()
        self.load_workers()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Сотрудники"))

        # Поисковая панель
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Поиск по специализации или телефону")
        self.search_btn = QPushButton("Поиск")
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(self.search_btn)
        layout.addLayout(search_layout)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.search_btn.clicked.connect(self.perform_search)

    def load_workers(self):
        self.all_workers = list_workers()
        self.show_workers(self.all_workers)

    def show_workers(self, workers):
        self.table.clear()
        self.table.setRowCount(len(workers))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Имя", "Специализация", "Телефон"])

        for row, worker in enumerate(workers):
            self.table.setItem(row, 0, QTableWidgetItem(str(worker.get("id", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(worker.get("name", "")))
            self.table.setItem(row, 2, QTableWidgetItem(worker.get("spec", "")))
            self.table.setItem(row, 3, QTableWidgetItem(worker.get("phone", "")))

    def perform_search(self):
        query = self.search_edit.text().strip().lower()
        if not query:
            self.show_workers(self.all_workers)
            return

        filtered = [
            w for w in self.all_workers
            if query in (w.get("spec") or "").lower() or query in (w.get("phone") or "")
        ]
        self.show_workers(filtered)

class WorksWidget(QWidget):
    def __init__(self, user=None):
        super().__init__()
        self.user = user
        self.init_ui()

    def init_ui(self):
        client = get_my_client(self.user['phone'])
        layout = QVBoxLayout()
        self.setLayout(layout)
        label = QLabel("Работы")
        layout.addWidget(label)

        table = QTableWidget()
        layout.addWidget(table)

        works = list_works()
        if self.user and self.user.get('role') == 'worker':
            works = [w for w in works if w.get('worker_id') == self.user['id']]
        elif self.user and self.user.get('role') == 'client':
            works = [w for w in works if w.get('order_id') in [o['id'] for o in list_orders() if o.get('client_id') == client.get('id')]]

        table.setRowCount(len(works))
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["ID", "Дата", "ID заказа", "ID сотрудника", "Стоимость"])

        for row, work in enumerate(works):
            table.setItem(row, 0, QTableWidgetItem(str(work.get("id", ""))))
            table.setItem(row, 1, QTableWidgetItem(str(work.get("done_by", ""))))
            table.setItem(row, 2, QTableWidgetItem(str(work.get("order_id", ""))))
            table.setItem(row, 3, QTableWidgetItem(str(work.get("worker_id", ""))))
            table.setItem(row, 4, QTableWidgetItem(str(work.get("price", ""))))

class WorkerProfileWidget(QWidget):
    def __init__(self, worker_phone):
        super().__init__()
        self.worker_phone = worker_phone
        self.init_ui()
        self.load_worker_data()

    def init_ui(self):
        self.setWindowTitle("Профиль сотрудника")
        layout = QVBoxLayout()

        self.name_edit = QLineEdit()
        self.job_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.spec_combo = QComboBox()
        self.save_button = QPushButton("Сохранить")

        layout.addWidget(QLabel("ФИО"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("Должность"))
        layout.addWidget(self.job_edit)
        layout.addWidget(QLabel("Специализация"))
        layout.addWidget(self.spec_combo)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.save_button.clicked.connect(self.save_profile)

    def load_worker_data(self):
        worker = get_worker_by_phone(self.worker_phone)
        if not worker:
            QMessageBox.warning(self, "Ошибка", "Профиль не найден")
            self.close()
            return

        self.name_edit.setText(worker.get("name", ""))
        self.job_edit.setText(worker.get("job", ""))
        self.phone_edit.setText(worker.get("phone", ""))

        specs = list_specs()
        spec_names = [spec.get("spec name", "") for spec in specs]

        self.spec_combo.addItems(spec_names)
        current_spec = worker.get("spec", "")
        if current_spec in spec_names:
            index = spec_names.index(current_spec)
            self.spec_combo.setCurrentIndex(index)

    def save_profile(self):
        try:
            name = self.name_edit.text()
            job = self.job_edit.text()
            spec = self.spec_combo.currentText()

            edit_worker(self.worker_phone, name, job, spec)
            QMessageBox.information(self, "Успех", "Профиль обновлен")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить профиль:\n{e}")

class ClientProfileWidget(QWidget):
    def __init__(self, client_phone):
        super().__init__()
        self.client_phone = client_phone
        self.init_ui()
        self.load_client_data()

    def init_ui(self):
        self.setWindowTitle("Профиль клиента")
        layout = QVBoxLayout()

        self.name_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.save_button = QPushButton("Сохранить")

        layout.addWidget(QLabel("Имя"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.email_edit)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.save_button.clicked.connect(self.save_profile)

    def load_client_data(self):
        client = get_client_by_phone(self.client_phone)
        if not client:
            QMessageBox.warning(self, "Ошибка", "Профиль не найден")
            self.close()
            return

        self.name_edit.setText(client.get("name", ""))
        self.phone_edit.setText(client.get("phone", ""))
        self.email_edit.setText(client.get("email", ""))

    def save_profile(self):
        try:
            name = self.name_edit.text()
            if validate_email(self.email_edit.text()): email = self.email_edit.text()
            else:
                QMessageBox.critical(self, "Ошибка", f"Неправильный формат email")
                email = ""

            edit_client(self.client_phone, name, email)
            QMessageBox.information(self, "Успех", "Профиль обновлен")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить профиль:\n{e}")


class DevicesManagerWidget(QWidget):
    def __init__(self, user=None):
        super().__init__()
        self.user = user
        self.client_id = None
        self.init_ui()
        self.resolve_client_id()
        self.load_devices()

    def resolve_client_id(self):
        if not self.user or not self.user.get("phone"):
            QMessageBox.critical(self, "Ошибка", "Телефон пользователя не задан")
            return
        client = get_my_client(self.user.get("phone"))
        if not client:
            QMessageBox.critical(self, "Ошибка", "Клиент по телефону не найден")
            return
        self.client_id = client.get("id")

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        layout.addWidget(QLabel("Управление устройствами"))

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Тип"])
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        layout.addLayout(btn_layout)

        self.add_btn = QPushButton("Добавить устройство")
        self.edit_btn = QPushButton("Редактировать выбранное")
        self.del_btn = QPushButton("Удалить выбранное")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.del_btn)

        self.add_btn.clicked.connect(self.add_device)
        self.edit_btn.clicked.connect(self.edit_device)
        self.del_btn.clicked.connect(self.delete_device)

    def load_devices(self):
        if not self.client_id:
            return
        devices = [d for d in list_devices() if d.get("client_id") == self.client_id]
        self.table.setRowCount(len(devices))
        for row, device in enumerate(devices):
            self.table.setItem(row, 0, QTableWidgetItem(str(device.get("id", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(device.get("name", "")))
            self.table.setItem(row, 2, QTableWidgetItem(device.get("type", "")))

    def get_selected_device_id(self):
        items = self.table.selectedItems()
        if not items:
            return None
        try:
            return int(items[0].text())
        except Exception:
            return None

    def add_device(self):
        spec_names = [spec.get("spec name") for spec in list_specs()]
        if not self.client_id:
            QMessageBox.warning(self, "Ошибка", "Не найден клиент")
            return

        name, ok = QInputDialog.getText(self, "Добавить устройство", "Название:")
        if not ok or not name:
            return

        type_, ok = QInputDialog.getItem(self, "Добавить устройство", "Тип:", spec_names, 0, editable=False)
        if not ok or not type_:
            return

        try:
            register_device(self.client_id, name, type_)
            QMessageBox.information(self, "Успех", "Устройство добавлено")
            self.load_devices()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить устройство:\n{e}")

    def edit_device(self):
        spec_names = [spec.get("spec name") for spec in list_specs()]
        dev_id = self.get_selected_device_id()
        if dev_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите устройство")
            return

        name, ok = QInputDialog.getText(self, "Редактировать устройство", "Новое название:")
        if not ok or not name:
            return

        type_, ok = QInputDialog.getItem(self, "Редактировать устройство", "Новый тип:", spec_names, editable=False)
        if not ok or not type_:
            return

        try:
            edit_device(dev_id, client_id=self.client_id, name=name, type_=type_)
            QMessageBox.information(self, "Успех", "Устройство обновлено")
            self.load_devices()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить устройство:\n{e}")

    def delete_device(self):
        dev_id = self.get_selected_device_id()
        if dev_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите устройство")
            return

        confirm = QMessageBox.question(self, "Подтверждение", "Удалить устройство?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                remove_device(dev_id)
                QMessageBox.information(self, "Успех", "Устройство удалено")
                self.load_devices()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить устройство:\n{e}")


class OrdersManagerWidget(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.init_ui()
        worker = get_my_worker(self.user.get('phone'))
        self.worker_id = worker.get('id')
        self.load_orders()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Управление заказами"))

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Статус", "Клиент ID", "Устройство ID", "Описание"])
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить заказ")
        self.edit_btn = QPushButton("Редактировать выбранный заказ")
        self.del_btn = QPushButton("Удалить заказ")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.del_btn)
        layout.addLayout(btn_layout)

        self.add_btn.clicked.connect(self.add_order)
        self.edit_btn.clicked.connect(self.edit_order)
        self.del_btn.clicked.connect(self.delete_order)

    def load_orders(self):
        orders = list_orders()
        filtered_orders = [o for o in orders if o.get('worker_id') == self.worker_id]

        self.table.setRowCount(len(filtered_orders))
        for row, order in enumerate(filtered_orders):
            self.table.setItem(row, 0, QTableWidgetItem(str(order.get("id", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(order.get("status", "")))
            self.table.setItem(row, 2, QTableWidgetItem(str(order.get("client_id", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(str(order.get("device_id", ""))))
            self.table.setItem(row, 4, QTableWidgetItem(order.get("description", "")))

    def get_selected_order_id(self):
        items = self.table.selectedItems()
        if not items:
            return None
        return int(items[0].text())

    def add_order(self):
        clients = sorted(list_clients(), key=lambda x: x.get("name", ""))
        client_display = [f"{c['id']} - {c['phone']}" for c in clients]
        client_map = {client_display[i]: clients[i]['id'] for i in range(len(clients))}

        client_item, ok = QInputDialog.getItem(self, "Новый заказ", "Выберите клиента:", client_display, editable=False)
        if not ok:
            return

        selected_client_id = client_map[client_item]
        devices = [d for d in list_devices() if d.get("client_id") == selected_client_id]
        devices = sorted(devices, key=lambda x: x.get("name", ""))
        device_display = [f"{d['id']} - {d['name']}" for d in devices]
        device_map = {device_display[i]: devices[i]['id'] for i in range(len(devices))}

        device_item, ok = QInputDialog.getItem(self, "Новый заказ", "Выберите устройство:", device_display,
                                               editable=False)
        if not ok:
            return

        status, ok = QInputDialog.getText(self, "Новый заказ", "Статус:")
        if not ok or not status:
            return

        description, ok = QInputDialog.getMultiLineText(self, "Новый заказ", "Описание:")
        if not ok:
            description = ""

        client_id = selected_client_id
        device_id = device_map[device_item]

        register_order(client_id, device_id, status, self.worker_id, description)
        QMessageBox.information(self, "Успех", "Заказ добавлен")
        self.load_orders()

    def edit_order(self):
        order_id = self.get_selected_order_id()
        if order_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ")
            return
        status, ok = QInputDialog.getText(self, "Редактировать заказ", "Новый статус:")
        if not ok or not status:
            return
        description, ok = QInputDialog.getMultiLineText(self, "Редактировать заказ", "Новое описание:")
        if not ok:
            description = ""

        edit_order(order_id, status=status, description=description)
        QMessageBox.information(self, "Успех", "Заказ обновлен")
        self.load_orders()

    def delete_order(self):
        order_id = self.get_selected_order_id()
        if order_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ")
            return
        confirm = QMessageBox.question(self, "Подтверждение", "Удалить заказ?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            remove_order(order_id)
            QMessageBox.information(self, "Успех", "Заказ удалён")
            self.load_orders()


class WorksManagerWidget(QWidget):
    def __init__(self, user):
        super().__init__()
        self.add_btn = None
        self.user = user
        self.worker_id = None
        self.init_ui()
        self.resolve_worker_id()
        self.load_works()

    def resolve_worker_id(self):
        phone = self.user.get('phone')
        if not phone:
            QMessageBox.critical(self, "Ошибка", "Телефон пользователя не задан")
            return
        worker = get_my_worker(phone)
        if not worker:
            QMessageBox.critical(self, "Ошибка", "Сотрудник по телефону не найден")
            return
        self.worker_id = worker.get('id')

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Управление работами"))

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Дата", "ID заказа", "ID сотрудника", "Стоимость"])
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Добавить работу")
        btn_layout.addWidget(self.add_btn)
        layout.addLayout(btn_layout)
        self.add_btn.clicked.connect(self.add_work)


    def load_works(self):
        if not self.worker_id:
            return
        works = list_works()
        works = [w for w in works if w.get('worker_id') == self.worker_id]

        self.table.setRowCount(len(works))
        for row, w in enumerate(works):
            self.table.setItem(row, 0, QTableWidgetItem(str(w.get("id", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(str(w.get("done_by", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(w.get("order_id", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(str(w.get("worker_id", ""))))
            self.table.setItem(row, 4, QTableWidgetItem(str(w.get("price", ""))))

    def get_selected_work_id(self):
        selected = self.table.selectedItems()
        if not selected:
            return None
        return int(selected[0].text())

    def add_work(self):
        if not self.worker_id:
            QMessageBox.warning(self, "Ошибка", "Не найден ID сотрудника")
            return
        orders = list_orders()
        if len(orders) == 0:
            QMessageBox.warning(self, "Ошибка", "Нет заказов")
            return
        clients = {c['id']: c for c in list_clients()}
        devices = {d['id']: d for d in list_devices()}

        order_display = []
        order_map = {}

        for o in orders:
            client = clients.get(o.get('client_id'))
            device = devices.get(o.get('device_id'))
            client_phone = client.get('phone') if client else "неизвестен"
            device_name = device.get('name') if device else "неизвестно"
            display_text = f"{o['id']} - Клиент: {client_phone}, Устройство: {device_name}"
            order_display.append(display_text)
            order_map[display_text] = o['id']

        order_item, ok = QInputDialog.getItem(self, "Новая работа", "Выберите заказ:", order_display, editable=False)
        if not ok:
            return

        price, ok = QInputDialog.getInt(self, "Новая работа", "Стоимость работы:", min=0)
        if not ok:
            return

        description, ok = QInputDialog.getMultiLineText(self, "Новая работа", "Описание:")
        if not ok:
            description = ""

        order_id = order_map[order_item]

        register_work(order_id, self.worker_id, price, description)
        QMessageBox.information(self, "Успех", "Работа добавлена")
        self.load_works()

    def delete_work(self):
        work_id = self.get_selected_work_id()
        if work_id is None:
            QMessageBox.warning(self, "Ошибка", "Выберите работу")
            return

        confirm = QMessageBox.question(
            self, "Удаление", "Вы уверены?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            remove_work(work_id)
            QMessageBox.information(self, "Успех", "Работа удалена")
            self.load_works()