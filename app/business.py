from .db import (
    add_client, update_client, delete_client, get_clients,
    add_device, update_device, delete_device, get_devices,
    add_order, update_order, delete_order, get_orders,
    add_worker, update_worker, delete_worker, get_workers,
    add_work, update_work, delete_work, get_works,
    get_users, add_user, update_user, delete_user, get_user_by_phone,
    get_specs, get_worker_by_phone, get_client_by_phone
)

# --- Clients ---
def register_client(name, phone, email=""):
    return add_client({"name": name, "phone": phone, "email": email})

def edit_client(client_phone, name=None, email=None):
    updated = {}
    if name is not None:
        updated["name"] = name
    if email is not None:
        updated["email"] = email
    return update_client(client_phone, updated)

def remove_client(client_id):
    return delete_client(client_id)

def list_clients():
    return get_clients()

# --- Devices ---
def register_device(client_id, name, type_=""):
    return add_device({"client_id": client_id, "name": name, "type": type_})

def edit_device(device_id, client_id=None, name=None, type_=None):
    updated = {}
    if client_id is not None:
        updated["client_id"] = client_id
    if name is not None:
        updated["name"] = name
    if type_ is not None:
        updated["type"] = type_
    return update_device(device_id, updated)

def remove_device(device_id):
    return delete_device(device_id)

def list_devices():
    return get_devices()

# --- Orders ---
def register_order(client_id, device_id, status, worker_id, description=None):
    return add_order({
        "client_id": client_id,
        "device_id": device_id,
        "status": status,
        "description": description,
        "worker_id": worker_id
    })

def edit_order(order_id, worker_id=None, client_id=None, device_id=None, status=None, description=None):
    updated = {}
    if client_id is not None:
        updated["client_id"] = client_id
    if device_id is not None:
        updated["device_id"] = device_id
    if worker_id is not None:
        updated["worker_id"] = worker_id
    if status is not None:
        updated["status"] = status
    if description is not None:
        updated["description"] = description
    return update_order(order_id, updated)

def remove_order(order_id):
    return delete_order(order_id)

def list_orders():
    return get_orders()

# --- Workers ---
def register_worker(name, job, spec="", phone=""):
    return add_worker({"name": name, "job": job, "spec": spec, "phone": phone})

def edit_worker(worker_phone, name=None, job=None, spec=None ):
    updated = {}
    if name is not None:
        updated["name"] = name
    if job is not None:
        updated["job"] = job
    if spec is not None:
        updated["spec"] = spec
    return update_worker(worker_phone, updated)

def remove_worker(worker_id):
    return delete_worker(worker_id)

def list_workers():
    return get_workers()

# --- Works ---
def register_work(order_id, worker_id, price, description=None):
    return add_work({
        "order_id": order_id,
        "worker_id": worker_id,
        "price": price,
        "description": description
    })

def edit_work(work_id, order_id=None, worker_id=None, price=None, description=None):
    updated = {}
    if order_id is not None:
        updated["order_id"] = order_id
    if worker_id is not None:
        updated["worker_id"] = worker_id
    if price is not None:
        updated["price"] = price
    if description is not None:
        updated["description"] = description
    return update_work(work_id, updated)

def remove_work(work_id):
    return delete_work(work_id)

def list_works():
    return get_works()

def register_user(name, phone, password_hash, role):
    user = add_user({"name": name, "phone": phone, "password_hash": password_hash, "role": role})
    if user and len(user) > 0:
        if role == "client":
            add_client({"name": name, "phone": phone})
        elif role == "worker":
            add_worker({"name": name, "job": "", "spec": "Не указано", "phone": phone})
    return user


def find_user_by_phone(phone):
    return get_user_by_phone(phone)

def list_specs():
    return get_specs()

def get_my_client(phone):
    return get_client_by_phone(phone)

def get_my_worker(phone):
    return get_worker_by_phone(phone)
