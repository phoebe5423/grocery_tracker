""" Specifies routing for the application"""
from flask import render_template, redirect, request, url_for, jsonify, flash
from app import app
from app import database as db_helper


@app.route("/product/")
def product_list():
    product_lst = db_helper.fetch_product()
    shopping_dict, list_name = db_helper.fetch_shopping_list()
    return render_template("product_list.html", product_lst=product_lst, list_name=list_name)



@app.route("/product-search", methods=["POST", "GET"])
def product_search():
    # if request.method == 'POST':
    search_word = request.form.get('search_word')
    product_lst = db_helper.fetch_product(search_word=search_word)
    shopping_dict, list_name = db_helper.fetch_shopping_list()

    return render_template('product_list.html', product_lst=product_lst, list_name=list_name)


@app.route("/product-delete/<string:prod_id>", methods=['POST', 'GET'])
def product_delete(prod_id):
    db_helper.remove_product_by_id(prod_id)
    # flash('Product deleted.')
    return redirect(url_for('product_list'))


@app.route('/product-update/', methods=['POST'])
def product_update():
    # if request.method == 'POST':
    prod_id = request.form.get('prod_id')
    prod_name = request.form.get('prod_name_edit')
    plu_code = request.form.get('plu_code_edit')
    lifespan = request.form.get('lifespan_edit')
    cal = request.form.get('cal_edit')
    db_helper.update_prod_entry(prod_id, prod_name, plu_code, lifespan, cal)
    # flash('Product updated successfully!')
    product_lst = db_helper.fetch_product(prod_id=prod_id)

    return redirect(url_for('product_list',product_lst=product_lst))


@app.route("/product-create", methods=['POST'])
def product_create():

    prod_name = request.form.get('prod_name')
    plu_code = request.form.get('plu_code')
    lifespan = request.form.get('lifespan')
    cal = request.form.get('cal')
    db_helper.insert_new_product(prod_name, plu_code, lifespan, cal)

    return redirect(url_for('product_list'))


@app.route('/product-to-inventory/', methods=['POST'])
def product_to_inventory():
    prod_id = request.form.get('prod_id')
    purch_date = request.form.get('purch_date')
    price = request.form.get('price')
    space = request.form.get('space')
    exp_date = request.form.get('exp_date')
    amount = request.form.get('amount')
    unit = request.form.get('unit')
    db_helper.insert_product_to_inventory(prod_id, purch_date, price, amount, unit, exp_date, space)
    return redirect(url_for('at_home'))


@app.route('/inventory-update/', methods=['POST'])
def inventory_update():
    inv_id = request.form.get('inv_id')
    item_name = request.form.get('inv_name_edit')
    space = request.form.get('space_edit')
    exp_date = request.form.get('date_edit')
    amount = request.form.get('amount_edit')
    unit = request.form.get('unit_edit')
    db_helper.update_inventory_entry(inv_id, item_name, space, exp_date, amount, unit)
    flash('Item updated successfully!')

    return redirect(url_for('at_home'))


@app.route('/inventory-delete/<string:inv_id>', methods=['POST', 'GET'])
def inventory_delete(inv_id):
    db_helper.remove_inventory_by_id(inv_id)
    return redirect(url_for('at_home'))


@app.route('/product-to-buy/', methods=['POST'])
def product_to_shopping():
    prod_id = request.form.get('prod_id')
    shopping_id = request.form.get('buy_list')
    amount = request.form.get('amount')
    unit = request.form.get('unit')
    db_helper.insert_product_to_shopping(shopping_id, prod_id, amount, unit)

    return redirect(url_for('to_buy'))

@app.route("/to_buy/")
def to_buy():
    shopping_dict, list_name = db_helper.fetch_shopping_list()

    return render_template("to_buy.html", shopping_dict=shopping_dict, list_name=list_name)

@app.route('/buy/item-update/', methods=['POST'])
def buy_item_update():

    shopping_id = request.form.get('shopping_id_edit')
    prod_id = request.form.get('prod_id_edit')
    prod_name = request.form.get('prod_name_edit')
    amount = request.form.get('amount_edit')
    unit = request.form.get('unit_edit')
    change_list = request.form.get('list_edit')

    db_helper.update_items_in_shopping_list(shopping_id, prod_id, prod_name, amount, unit, change_list)

    return redirect(url_for('to_buy'))


@app.route('/buy/list-update/', methods=['POST'])
def buy_list_update():
    shopping_id = request.form.get('shopping_id_edit')
    list_name = request.form.get('list_name_edit')
    db_helper.update_shopping_list(list_name, shopping_id)
    return redirect(url_for('to_buy'))


@app.route('/buy/list-create/', methods=['POST'])
def buy_list_create():
    list_name = request.form.get('list_name_create')
    db_helper.create_shopping_list(list_name)
    return redirect(url_for('to_buy'))

@app.route('/buy/list-delete/<int:shopping_id>', methods=['POST', 'GET'])
def buy_list_delete(shopping_id):

    db_helper.delete_shopping_list(shopping_id)
    return redirect(url_for('to_buy'))


@app.route('/buy/item-delete/<int:shopping_id>-<string:prod_id>', methods=['POST', 'GET'])
def buy_item_delete(shopping_id, prod_id):
    db_helper.remove_items_in_shopping_list(shopping_id, prod_id)
    # flash('Item deleted.')
    return redirect(url_for('to_buy'))


@app.route("/store/search", methods=["POST", "GET"])
def store_search():
    if request.method == 'POST':
        search_word = request.form.get('search_word')
        store_lst = db_helper.fetch_store(search=True, search_word=search_word)
    else:
        store_lst = db_helper.fetch_store()

    return render_template('find_stores.html', store_lst=store_lst)


@app.route("/store/create", methods=['POST'])
def store_create():
    """ recieves post requests to add new task """
    if request.method == 'POST':
        store_name = request.form.get('store_name')
        open_hr = request.form.get('open_hr')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        postal = request.form.get('postal')
        phone = request.form.get('phone')
        db_helper.insert_new_store(store_name, open_hr, address, city, state, postal, phone)
        # flash('New store %s created successfully!' % store_name)
        return redirect(url_for('find_stores'))


@app.route('/store/update/', methods=['POST'])
def store_update():
    if request.method == 'POST':
        store_id = request.form.get('store_id')
        store_name = request.form.get('store_name_edit')
        open_hr = request.form.get('open_hr_edit')
        address = request.form.get('address_edit')
        city = request.form.get('city_edit')
        state = request.form.get('state_edit')
        postal = request.form.get('postal_edit')
        phone = request.form.get('phone_edit')

        db_helper.update_store_entry(store_id, store_name, open_hr, address, city, state, postal, phone)
        # flash('Store %s updated successfully!' % store_name)

        return redirect(url_for('find_stores'))


@app.route("/store/delete/<string:store_id>", methods=['POST', 'GET'])
def store_delete(store_id):
    db_helper.remove_store_by_id(store_id)
    # flash('Store deleted.')
    return redirect(url_for('find_stores'))


@app.route("/")
def homepage():
    inv_fridge_lst, inv_freezer_lst, inv_pantry_lst = db_helper.fetch_inventory()
    return render_template("at_home.html", fridge=inv_fridge_lst, freezer=inv_freezer_lst, pantry=inv_pantry_lst)


@app.route("/at_home/")
def at_home():
    inv_fridge_lst, inv_freezer_lst, inv_pantry_lst = db_helper.fetch_inventory()
    return render_template("at_home.html", fridge=inv_fridge_lst, freezer=inv_freezer_lst, pantry=inv_pantry_lst)


@app.route("/find_stores/")
def find_stores():
    store_lst = db_helper.fetch_store()
    return render_template('find_stores.html', store_lst=store_lst)


# @app.route("/dashboard/")
# def dashboard():
#     """ returns rendered page """
#     product_lst = db_helper.fetch_product()
#     shopping_lst = db_helper.fetch_shopping_list()
#     return render_template("product_list.html", product_lst=product_lst, shopping_lst=shopping_lst)
