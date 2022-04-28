"""Defines all the functions related to the database"""
from app import db
import random


def fetch_product(search_word=None) -> list:
    """Reads all items listed in the Product table

    :return: A list of dictionaries
    """
    query = "Select * from Product order by ProductName;"
    if search_word in ['all', 'All', 'ALL', ' ', '']:
        query = "Select * from Product order by ProductName;"
    elif search_word is not None:

        query = "Select * from Product where ProductName like '%s' order by ProductName;" % ('%%' + search_word + '%%')

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
        if ct > 50:
            break

    return product_lst


def fetch_procedure_minPriceArea(prod_id):

    connection = db.raw_connection()
    cursor = connection.cursor()
    cursor.callproc("minPriceArea", [prod_id, ])
    results = cursor.fetchall()
    cursor.close()

    if len(results) ==0:
        return ("na","na",0)

    return results[0]

def fetch_procedure_sumShoppingList(shopping_id, prod_id):
    if prod_id is None:
        return 0
    connection = db.raw_connection()
    cursor = connection.cursor()
    cursor.callproc("sumShoppingList", [shopping_id, ])
    results = cursor.fetchone()
    cursor.close()

    return results[0]


def fetch_shopping_list(customer_id='27') -> list:
    conn = db.connect()
    query = "SELECT lst.ShoppingID, ListName, inc.ProductID, ProductName, Amount, Unit, ItemName " \
            "FROM ShoppingList lst left Join include inc on lst.ShoppingID = inc.ShoppingID " \
            "left Join Product prd on inc.ProductID = prd.ProductID where CustomerID='{}';".format(customer_id)

    query_results = conn.execute(query).fetchall()
    conn.close()
    shopping_dict = {}
    same_id_dit = {"list_name": None, "shop_items": []}
    list_name = []
    shopping_id_current = None
    for result in query_results:
        shopping_id_next = result[0]

        prod_id = result[2]
        if prod_id is None:
            lst = { }

        else:

            store_id, store_name, avg_price = fetch_procedure_minPriceArea(result[2])

            prod_name = result[-1]
            if prod_name is None:
                prod_name = result[3]

            lst = {
                "shopping_id": result[0],
                "list_name": result[1],
                "prod_id": result[2],
                "prod_name": prod_name,
                "amount": result[4],
                "unit": result[5],
                "store_recomnd_id": store_id,
                "store_recomnd": store_name,
                "avg_price": round(avg_price,2)
            }
        if shopping_id_current is not None and shopping_id_next != shopping_id_current:

            if same_id_dit["shop_items"][0] != {}:
                total_est_price = fetch_procedure_sumShoppingList(shopping_id_current, same_id_dit["shop_items"][-1]["prod_id"])
            list_info = {"shopping_id": shopping_id_current, "list_name": same_id_dit["list_name"]}
            list_name.append(list_info)
            same_id_dit["total_est_price"] = total_est_price
            shopping_dict[shopping_id_current] = same_id_dit
            same_id_dit = {"list_name": None, "shop_items": []}

        same_id_dit["list_name"] = result[1]
        same_id_dit["shop_items"] += [lst]
        shopping_id_current = shopping_id_next


    list_info = {"shopping_id": shopping_id_current, "list_name": same_id_dit["list_name"]}
    list_name.append(list_info)

    total_est_price = fetch_procedure_sumShoppingList(shopping_id_current, prod_id)
    same_id_dit["total_est_price"] = total_est_price
    shopping_dict[shopping_id_current] = same_id_dit

    query_prod = "SELECT ProductID FROM ShoppingList natural Join include Where ShoppingID ='{}' ;".format(3)

    conn = db.connect()
    prod_lst = conn.execute(query_prod).fetchall()
    conn.close()


    return shopping_dict, list_name

def create_shopping_list(list_name, customer_id='27'):

    query = "SELECT ShoppingID FROM ShoppingList order by ShoppingID desc limit 1 ;"

    conn = db.connect()
    id = conn.execute(query).fetchone()[0]
    new_id = int(id)+1

    insert = 'Insert Into ShoppingList (ShoppingID, CustomerID, ListName) ' \
             'VALUES ("{}", "{}", "{}");'.format(new_id, customer_id, list_name)
    conn.execute(insert)
    conn.close()

def delete_shopping_list(shopping_id, customer_id='27'):
    query_prod = "SELECT ProductID FROM ShoppingList natural Join include Where ShoppingID ='{}' ;".format(shopping_id)
    conn = db.connect()
    prod_lst = conn.execute(query_prod).fetchall()
    print("prod_lst",prod_lst)

    for prod in prod_lst:
        prod_id = prod[0]
        query_delete_prod = 'Delete From include  where ShoppingID = "{}" and ProductID = "{}";'.format(shopping_id,
                                                                                                        prod_id)
        conn.execute(query_delete_prod)

    query_delete_list = 'Delete From ShoppingList where ShoppingID = "{}" and CustomerID = "{}";'.format(shopping_id, customer_id)

    conn.execute(query_delete_list)



def update_shopping_list(list_name, shopping_id, customer_id='27'):
    conn = db.connect()
    query = 'Update ShoppingList Set ListName= "{}" Where ShoppingID = "{}" and CustomerID = "{}";'.format(
        list_name, shopping_id, customer_id)
    conn.execute(query)
    conn.close()

def update_items_in_shopping_list(shopping_id, prod_id, prod_name, amount, unit, change_to_id, customer_id='27'):

    conn = db.connect()
    query = 'Update include Set ShoppingID="{}", ItemName= "{}", Amount = "{}",Unit="{}" ' \
            'Where ShoppingID = "{}" and ProductID = "{}";'.format(
        int(change_to_id), prod_name, amount, unit, int(shopping_id), prod_id)
    conn.execute(query)
    conn.close()

def remove_items_in_shopping_list(shopping_id, prod_id):
    conn = db.connect()
    query = 'Delete From include where ShoppingID = "{}" and ProductID = "{}";'.format(shopping_id,prod_id)
    conn.execute(query)
    conn.close()


def fetch_inventory(customer_id='27') -> dict:
    """Reads all items listed in the Product table

    :return: A list of dictionaries
    """

    conn = db.connect()
    query = "select * from InventoryList natural join Product where CustomerID='{}' order by ExpirationDate;".format(
        customer_id)
    query_results = conn.execute(query).fetchall()


    conn.close()
    inv_fridge_lst = []
    inv_freezer_lst = []
    inv_pantry_lst = []

    for result in query_results:
        if result[3] is None:
            prod_name = result[-2]
        else:
            prod_name = result[3]

        inv_item = {
            "inv_id": result[1],
            "item_name": prod_name,
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

    return inv_fridge_lst, inv_freezer_lst, inv_pantry_lst


def insert_product_to_inventory(prod_id, purch_date, price, amount, unit, exp_date, space, customer_id='27') -> None:
    print("input", prod_id, purch_date, price, amount, unit, exp_date, space )

    conn = db.connect()
    query_purch_id = conn.execute("Select PurchaseID from Purchase order by PurchaseID desc limit 1;").fetchone()
    purch_id = str(int(query_purch_id[0]) + 1)
    print("query_purch_id",query_purch_id,"purch_id",purch_id)

    query_inv_id = conn.execute("Select InventoryID from InventoryList order by InventoryID desc limit 1;").fetchone()
    inv_id = int(query_inv_id[0]) + 1
    print("query_inv_id", query_inv_id, "inv_id", inv_id)

    query_insert_purchase = 'Insert Into Purchase (PurchaseID, InventoryID, PurchaseDate, CustomerID) ' \
                            'VALUES ("{}", "{}", "{}", "{}");'.format(
        purch_id, inv_id, purch_date,customer_id )
    conn.execute(query_insert_purchase)

    query_insert_has = 'Insert Into Has (H_purchaseID, H_productID, Price, Amount, Unit,ExpirationDate,StorageSpace) ' \
                            'VALUES ("{}", "{}", "{}", "{}","{}","{}","{}");'.format(
        purch_id, prod_id, float(price), int(amount), unit, exp_date,space)
    conn.execute(query_insert_has)

    conn.close()


def update_inventory_entry(inv_id, item_name, space, exp_date, amount, unit) -> None:
    conn = db.connect()
    query = 'Update InventoryList Set ItemName="{}", ExpirationDate= "{}", StorageSpace= "{}", Amount = "{}",Unit="{}" Where InventoryID = "{}";'.format(
        item_name, exp_date, space, amount, unit, inv_id)

    conn.execute(query)
    conn.close()


def remove_inventory_by_id(inv_id) -> None:
    conn = db.connect()
    # print(inv_id)
    query = 'Delete From InventoryList where InventoryID="{}";'.format(inv_id)
    conn.execute(query)
    conn.close()


def insert_product_to_shopping(shopping_id, prod_id, amount, unit, customer_id='27') -> None:
    conn = db.connect()
    query_include = 'Insert Into include (ShoppingID, ProductID, Amount, Unit) ' \
                    'VALUES ("{}", "{}", "{}", "{}");'.format(shopping_id, prod_id, amount, unit)
    conn.execute(query_include)
    conn.close()


def update_buy_items(shopping_id, prod_id, prod_name, amount, unit, customer_id='27') -> None:
    conn = db.connect()
    query = 'Update include Set Amount = "{}",Unit="{}",ItemName="{}" Where ShoppingID = "{}" and ProductID="{}";'.format(
        amount, unit, prod_name, shopping_id, prod_id)
    conn.execute(query)
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
    query = 'Insert Into Product (ProductID, ProductName, PLUcode, Lifespan, Calories) VALUES ("{}", "{}", "{}", "{}","{}");'.format(
        str(new_id), prod_name, plu_code, lifespan, cal)
    conn.execute(query)
    conn.close()
    return str(new_id)


def remove_product_by_id(prod_id) -> None:
    conn = db.connect()
    query = 'Delete From Product where ProductID="{}";'.format(prod_id)
    conn.execute(query)
    conn.close()


def fetch_store(search=False, search_word=None) -> dict:
    if search:
        # print("search word: [[{}]]".format(search_word))
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
