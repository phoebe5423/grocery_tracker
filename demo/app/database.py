"""Defines all the functions related to the database"""
from app import db
import random


def fetch_product(search=False, search_word=None) -> dict:
    """Reads all items listed in the Product table

    :return: A list of dictionaries
    """
    if search:
        print("search word: [[{}]]".format(search_word))
        query = "Select * from Product where ProductName like '%s' order by ProductName;" % ('%%' + search_word + '%%')
    else:
        query = "Select * from Product order by ProductName;"

    conn = db.connect()
    query_results = conn.execute(query).fetchall()
    conn.close()
    product_lst = []

    ct = 0
    for result in query_results:
        item = {
            "prod_id": result[0],
            "prod_name": result[5],
            "plu_code": result[1],
            "lifespan": result[2],
            "cal": result[3]
        }

        product_lst.append(item)
        ct += 1
        if ct > 30:
            break

    return product_lst


def fetch_inventory(customer_id='125') -> dict:
    """Reads all items listed in the Product table

    :return: A list of dictionaries
    """
    pass
    conn = db.connect()
    query = "select * from InventoryList natural join Product where customerid='{}';".format(customer_id)
    query_results = conn.execute(query).fetchall()
    conn.close()
    inv_fridge_lst = []
    inv_freezer_lst = []
    inv_pantry_lst = []
    for result in query_results:
        print(result)
        inv_item = {
            "inv_id": result[0],
            "item_name": result[-2],
            "space": result[4],
            "amount": result[5],
            "unit": result[6],
            "exp_date": result[3]
        }
        if inv_item['space'] == 'Fridge':
            inv_fridge_lst.append(inv_item)
        elif inv_item['space'] == 'Freezer':
            inv_freezer_lst.append(inv_item)
        else:
            inv_pantry_lst.append(inv_item)

    return inv_fridge_lst, inv_freezer_lst, inv_pantry_lst


def update_prod_entry(prod_id, prod_name, plu_code, lifespan, cal) -> None:
    """Updates task description based on given `task_id`

    Args:
        prod_id (int): Targeted task_id
        data (str): Updated description

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update Product Set ProductName= "{}", PLUcode= "{}", Lifespan = "{}",Calories="{}" Where ProductID = "{}";'.format(
        prod_name, plu_code, lifespan, cal, prod_id)

    conn.execute(query)
    conn.close()


def insert_new_product(prod_name, plu_code, lifespan, cal) -> int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """
    conn = db.connect()
    query_results = conn.execute("Select ProductID from Product;").fetchall()
    prod_id_lst = []

    for result in query_results:
        prod_id_lst.append(result[0])

    rand_id = str(12345)
    while rand_id in prod_id_lst:
        rand_id = str(random.randint(10000, 99999))
    # print(rand_id)

    query = 'Insert Into Product (ProductID, ProductName, PLUcode, Lifespan, Calories) VALUES ("{}", "{}", "{}", "{}","{}");'.format(
        rand_id, prod_name, plu_code, lifespan, cal)
    conn.execute(query)
    conn.close()


def remove_product_by_id(prod_id) -> None:
    """ remove entries based on task ID """

    conn = db.connect()
    query = 'Delete From Product where ProductID="{}";'.format(prod_id)
    conn.execute(query)
    conn.close()


def fetch_store(search=False, search_word=None) -> dict:

    if search:
        print("search word: [[{}]]".format(search_word))
        query = "Select * from Store where StoreName like '%s' order by StoreName;" % ('%%' + search_word + '%%')

    else:
        query = "Select * from Store order by StoreName;"

    conn = db.connect()
    query_results = conn.execute(query).fetchall()
    conn.close()
    store_lst = []

    ct = 0
    for result in query_results:
        phone_num = "(%s)%s-%s" % (result[2][:3],result[2][3:6],result[2][5:])

        item = {
            "store_id": result[0],
            "store_name": result[1],
            "open_hr": result[4],
            "address": result[3],
            "city": result[5],
            "state": result[6],
            "postal": result[7],
            "phone": phone_num,
        }

        store_lst.append(item)
        ct += 1
        if ct > 30:
            break

    return store_lst


def insert_new_store(store_name, open_hr, address, city, state, postal, phone) -> int:

    conn = db.connect()
    query_results = conn.execute("Select StoreId from Store;").fetchall()
    id_lst = []

    for result in query_results:
        id_lst.append(result[0])

    rand_id = str(1234)
    while rand_id in id_lst:
        rand_id = str(random.randint(1000, 9999))
    # print(rand_id)

    query = 'Insert Into Store (StoreId, StoreName, OpenHours, Address, City, State, PostalCode, PhoneNumber) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");'.format(
        rand_id, store_name, open_hr, address, city, state, postal, phone)
    conn.execute(query)
    conn.close()


def update_store_entry(store_id, store_name, open_hr, address, city, state, postal, phone) -> None:

    conn = db.connect()
    query = 'Update Store Set StoreName="{}", OpenHours="{}", Address="{}", City="{}", State="{}", PostalCode="{}", PhoneNumber="{}" Where StoreId = "{}";'.format(
        store_name, open_hr, address, city, state, postal, phone, store_id)
    conn.execute(query)
    conn.close()


def remove_store_by_id(store_id) -> None:

    conn = db.connect()
    query = 'Delete From Store where StoreId="{}";'.format(store_id)
    conn.execute(query)
    conn.close()