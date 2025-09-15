from supabase import create_client
from .config import get_supabase_config

SUPABASE_URL, SUPABASE_KEY = get_supabase_config()
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Clients ---
def get_clients():
    return supabase.table("clients").select("*").execute().data

def add_client(client_data):
    return supabase.table("clients").insert(client_data).execute().data

def update_client(client_phone, updated_data):
    return supabase.table("clients").update(updated_data).eq("phone", client_phone).execute().data

def delete_client(client_id):
    return supabase.table("clients").delete().eq("id", client_id).execute().data

# --- Devices ---
def get_devices():
    return supabase.table("devices").select("*").execute().data

def add_device(device_data):
    return supabase.table("devices").insert(device_data).execute().data

def update_device(device_id, updated_data):
    return supabase.table("devices").update(updated_data).eq("id", device_id).execute().data

def delete_device(device_id):
    return supabase.table("devices").delete().eq("id", device_id).execute().data

# --- Orders ---
def get_orders():
    return supabase.table("orders").select("*").execute().data

def add_order(order_data):
    return supabase.table("orders").insert(order_data).execute().data

def update_order(order_id, updated_data):
    return supabase.table("orders").update(updated_data).eq("id", order_id).execute().data

def delete_order(order_id):
    return supabase.table("orders").delete().eq("id", order_id).execute().data

# --- Workers ---
def get_workers():
    return supabase.table("workers").select("*").execute().data

def add_worker(worker_data):
    return supabase.table("workers").insert(worker_data).execute().data

def update_worker(worker_phone, updated_data):
    return supabase.table("workers").update(updated_data).eq("phone", worker_phone).execute().data

def delete_worker(worker_id):
    return supabase.table("workers").delete().eq("id", worker_id).execute().data

# --- Works ---
def get_works():
    return supabase.table("works").select("*").execute().data

def add_work(work_data):
    return supabase.table("works").insert(work_data).execute().data

def update_work(work_id, updated_data):
    return supabase.table("works").update(updated_data).eq("id", work_id).execute().data

def delete_work(work_id):
    return supabase.table("works").delete().eq("id", work_id).execute().data

# --- Users ---
def get_users():
    return supabase.table("users").select("*").execute().data

def add_user(user_data):
    response = supabase.table("users").insert(user_data).execute()
    if response.data is None or (isinstance(response.data, dict) and 'message' in response.data):
        raise Exception(f"Supabase error: {response.data}")
    return response.data

def update_user(user_id, updated_data):
    return supabase.table("users").update(updated_data).eq("id", user_id).execute().data

def delete_user(user_id):
    return supabase.table("users").delete().eq("id", user_id).execute().data

def get_user_by_phone(phone):
    resp = supabase.table("users").select("*").eq("phone", phone).execute()
    data = resp.data
    if data and len(data) > 0:
        return data[0]
    return None

# --- Specs ---
def get_specs():
    return supabase.table("specs").select("*").execute().data

def get_client_by_phone(phone):
    resp = supabase.table("clients").select("*").eq("phone", phone).execute()
    return resp.data[0] if resp.data else None

def get_worker_by_phone(phone):
    resp = supabase.table("workers").select("*").eq("phone", phone).execute()
    return resp.data[0] if resp.data else None

def get_worker_by_id(worker_id):
    resp = supabase.table("workers").select("*").eq("id", worker_id).single().execute()
    return resp.data if resp.data else None

def get_client_by_id(client_id):
    resp = supabase.table("clients").select("*").eq("id", client_id).single().execute()
    return resp.data if resp.data else None
