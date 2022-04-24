"""Defines all the functions related to the database"""
from app import db
import random


def fetch_product(search=False, search_word=None) -> dict:
    """Reads all items listed in the Product table

    :return: A list of dictionaries
    """
    if search in ['all', 'All', 'ALL', ' ', '']:
        query = "Select * from Product order by ProductName;"
    elif search:
        query = "Select * from Product where ProductName like '%s' order by ProductName;" % ('%%' + search_word + '%%')
    else:
        return None

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

def fetch_shopping_list(customer_id='27') -> dict:

    conn = db.connect()
    query = "select * from ShoppingList where customerid='{}';".format(customer_id)
    query_results = conn.execute(query).fetchall()
    conn.close()
    shopping_lst = []

    for result in query_results:
        lst = {
            "shopping_id": result[0],
            "list_name": result[2],
        }

        shopping_lst.append(lst)

    return shopping_lst

def fetch_inventory(customer_id='27') -> dict:
    """Reads all items listed in the Product table

    :return: A list of dictionaries
    """

    conn = db.connect()
    # query = "select * from InventoryList natural join Product order by ExpirationDate;"
    # query = "select * from InventoryList natural join Product order by InventoryID desc;"
    query = "select * from InventoryList natural join Product where customerid='{}' order by ExpirationDate;".format(
        customer_id)
    query_results = conn.execute(query).fetchall()
    conn.close()
    inv_fridge_lst = []
    inv_freezer_lst = []
    inv_pantry_lst = []

    for result in query_results:
        # print(result)
        inv_item = {
            "inv_id": result[1],
            "item_name": result[-2],
            "space": result[5],
            "amount": result[6],
            "unit": result[7],
            "exp_date": result[4]
        }

        if inv_item['space'] == 'Fridge':
            inv_fridge_lst.append(inv_item)
        elif inv_item['space'] == 'Freezer':
            inv_freezer_lst.append(inv_item)
        else:
            inv_pantry_lst.append(inv_item)

        # insert = """UPDATE InventoryList SET ItemName = %s WHERE InventoryID = %s;""" % ('%'+inv_item['item_name']+'%', '%'+inv_item['inv_id']+'%')
    #     name, id = inv_item['item_name'], inv_item['inv_id']
    #     if int(id[0:3]) < 631 and "Milk" not in name and " Cream" not in name:
    #
    #         insert = "UPDATE InventoryList SET ItemName = %s WHERE InventoryID = %s;" % (
    #             '"' + name + '"', '"' + id + '"')
    #         print(insert)
    #         conn.execute(insert)
    # conn.close()

    return inv_fridge_lst, inv_freezer_lst, inv_pantry_lst


def insert_product_to_inventory(prod_id, space, exp_date, amount, unit, customer_id='27') -> None:

    conn = db.connect()
    query_results = conn.execute("Select InventoryID from InventoryList order by InventoryID desc limit 1;").fetchall()

    new_id = int(query_results[0][0]) + 1

    query = 'Insert Into InventoryList (InventoryID, CustomerID, ProductID, ExpirationDate, StorageSpace, Amount, Unit) ' \
            'VALUES ("{}", "{}", "{}", "{}","{}","{}","{}");'.format(
        str(new_id), customer_id, prod_id, exp_date, space, amount, unit)
    conn.execute(query)
    conn.close()


def update_inventory_entry(inv_id, space, exp_date, amount, unit) -> None:
    conn = db.connect()
    query = 'Update InventoryList Set ExpirationDate= "{}", StorageSpace= "{}", Amount = "{}",Unit="{}" Where InventoryID = "{}";'.format(
        exp_date, space, amount, unit, inv_id)

    conn.execute(query)
    conn.close()


def remove_inventory_by_id(inv_id) -> None:
    conn = db.connect()
    query = 'Delete From InventoryList where InventoryID="{}";'.format(inv_id)
    conn.execute(query)
    conn.close()

def insert_product_to_shopping(prod_id, shopping_id, amount, unit, customer_id='27') -> None:
    # TODO: if new shopping list or existing list

    conn = db.connect()
    query_results = conn.execute("Select ShoppingID from ShoppingList order by ShoppingID desc limit 1;").fetchall()
    id_list = [] # fetch primary keys
    newid = int(query_results[0][0]) + 1

    query_include = 'Insert Into include (ShoppingID, ProductID, Amount, Unit) ' \
            'VALUES ("{}", "{}", "{}", "{}");'.format(
        shopping_id,prod_id,amount,unit)
    conn.execute(query_include)
    conn.close()

def update_prod_entry(prod_id, prod_name, plu_code, lifespan, cal) -> None:
    conn = db.connect()
    query = 'Update Product Set ProductName= "{}", PLUcode= "{}", Lifespan = "{}",Calories="{}" Where ProductID = "{}";'.format(
        prod_name, plu_code, lifespan, cal, prod_id)

    conn.execute(query)
    conn.close()


def insert_new_product(prod_name, plu_code, lifespan, cal):
    conn = db.connect()
    query_results = conn.execute("Select ProductID from Product order by ProductID desc limit 1;").fetchall()

    new_id = int(query_results[0][0]) + 1

    # prod_id_lst = []
    # for result in query_results:
    #     prod_id_lst.append(result[0])
    #
    # new_id = 10000
    # while str(new_id) in prod_id_lst:
    #     new_id += 1
    # if str(new_id) in prod_id_lst:
    #     rand_id = str(random.randint(10000, 99999))

    query = 'Insert Into Product (ProductID, ProductName, PLUcode, Lifespan, Calories) VALUES ("{}", "{}", "{}", "{}","{}");'.format(
        str(new_id), prod_name, plu_code, lifespan, cal)
    conn.execute(query)
    conn.close()


def remove_product_by_id(prod_id) -> None:
    conn = db.connect()
    query = 'Delete From Product where ProductID="{}";'.format(prod_id)
    conn.execute(query)
    conn.close()


def fetch_store(search=False, search_word=None) -> dict:
    if search:
        print("search word: [[{}]]".format(search_word))
        query = "Select * from Store where StoreName like '%s' order by StoreId desc, State, StoreName;" % (
                '%%' + search_word + '%%')

    else:
        query = "Select * from Store order by State desc, StoreId, StoreName;"

    conn = db.connect()
    query_results = conn.execute(query).fetchall()
    conn.close()
    store_lst = []

    ct = 0
    for result in query_results:
        phone_num = "(%s)%s-%s" % (result[2][:3], result[2][3:6], result[2][5:])

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
    query_results = conn.execute("Select StoreId from Store order by StoreId desc limit 1;").fetchall()

    new_id = query_results[0][0] + 1

    query = 'Insert Into Store (StoreId, StoreName, OpenHours, Address, City, State, PostalCode, PhoneNumber) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");'.format(
        new_id, store_name, open_hr, address, city, state, postal, phone)
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
