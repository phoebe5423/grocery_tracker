""" Specifies routing for the application"""
from flask import render_template, redirect, request, url_for, jsonify, flash
from app import app
from app import database as db_helper


@app.route("/product/search", methods=["POST", "GET"])
def product_search():
    if request.method == 'POST':
        search_word = request.form.get('search_word')
        print(search_word)

        product_lst = db_helper.fetch_product(search=True, search_word=search_word)

    else:
        product_lst = db_helper.fetch_product()
    return render_template('all_items.html', product_lst=product_lst)


@app.route("/product/delete/<string:prod_id>", methods=['POST', 'GET'])
def product_delete(prod_id):
    db_helper.remove_product_by_id(prod_id)
    flash('Product deleted.')
    return redirect(url_for('product_list'))


@app.route('/product/update/', methods=['POST'])
def product_update():
    if request.method == 'POST':
        prod_id = request.form.get('prod_id')
        prod_name = request.form.get('prod_name_edit')
        plu_code = request.form.get('plu_code_edit')
        lifespan = request.form.get('lifespan_edit')
        cal = request.form.get('cal_edit')
        db_helper.update_prod_entry(prod_id, prod_name, plu_code, lifespan, cal)
        flash('Product updated successfully!')

        return redirect(url_for('product_list'))


@app.route("/product/create", methods=['POST'])
def product_create():
    """ recieves post requests to add new task """
    if request.method == 'POST':
        prod_name = request.form.get('prod_name')
        plu_code = request.form.get('plu_code')
        lifespan = request.form.get('lifespan')
        cal = request.form.get('cal')
        db_helper.insert_new_product(prod_name, plu_code, lifespan, cal)
        flash('Product created successfully!')
        return redirect(url_for('product_list'))


@app.route("/store/search", methods=["POST", "GET"])
def store_search():
    if request.method == 'POST':
        search_word = request.form.get('search_word')
        print(search_word)

        store_lst = db_helper.fetch_store(search=True, search_word=search_word)

    else:
        store_lst = db_helper.fetch_store()

    return render_template('find_store.html', store_lst=store_lst)


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
        flash('New store %s created successfully!' % store_name)
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
        flash('Store %s updated successfully!' % store_name)

        return redirect(url_for('find_stores'))

@app.route("/store/delete/<string:store_id>", methods=['POST', 'GET'])
def store_delete(store_id):
    db_helper.remove_store_by_id(store_id)
    flash('Store deleted.')
    return redirect(url_for('find_stores'))

@app.route("/")
def homepage():
    """ returns rendered homepage """
    return render_template("index.html")


@app.route("/product/")
def product_list():
    """ returns rendered page """
    product_lst = db_helper.fetch_product()
    return render_template("all_items.html", product_lst=product_lst)

@app.route("/at_home/")
def at_home():
    """ returns rendered page """

    inv_fridge_lst, inv_freezer_lst, inv_pantry_lst = db_helper.fetch_inventory()
    return render_template("at_home.html", fridge=inv_fridge_lst, freezer=inv_freezer_lst, pantry=inv_pantry_lst)

@app.route("/to_buy/")
def to_buy():
    """ returns rendered page """
    # TODO: fetch
    items = db_helper.fetch_product()
    return render_template("to_buy.html", items=items)


@app.route("/find_stores/")
def find_stores():
    """ returns rendered page """
    store_lst = db_helper.fetch_store()
    return render_template('find_stores.html', store_lst=store_lst)



@app.route("/dashboard/")
def dashboard():
    """ returns rendered page """
    # TODO: fetch
    items = db_helper.fetch_product()
    return render_template("dashboard.html", items=items)
