import os
import shutil
from flask import Flask, render_template, request

app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deleteproduct', methods=['POST'])
def deleteproduct():
    selected_folders = request.form.getlist("delete")
    for product in selected_folders:
        shutil.rmtree("products/"+product)
    products_list = []
    products_dir = "products"
    products = os.listdir(products_dir)
    products = [product for product in products if os.path.isdir(products_dir+'/'+product)]
    for product in products:
        ingridients = open(products_dir+'/'+product+'/ingridients', 'r').read()
        container = open(products_dir+'/'+product+'/container', 'r').read()
        selling_price = float(open(products_dir+'/'+product+'/selling_price', 'r').read())
        skimmed_milk_quantity, fat_quantity = [float(element) for element in ingridients.split(',')]
        size, container_price = [float(element) for element in container.split(',')]
        fat_quantity = float(fat_quantity) * 100
        products_list.append([product, skimmed_milk_quantity, fat_quantity, size, container_price, selling_price])
    return render_template('productslist.html', products=products_list)

@app.route('/calculate')
def calculate():
    products_list = []
    products_dir = "products"
    products = os.listdir(products_dir)
    products = [product for product in products if os.path.isdir(products_dir+'/'+product)]
    for product in products:
        products_list.append(product)
    return render_template('calculate.html', products=products_list)

@app.route('/matrix', methods=['POST'])
def matrix():
    product_bounds = []
    products_dir = "work"
    products = os.listdir(products_dir)
    products = [product for product in products if os.path.isdir(products_dir+'/'+product)]
    for product in products:
        shutil.rmtree("work/"+product)
    use = request.form.getlist("use")
    for product in use:
        shutil.copytree("products/"+product, "work/"+product)
        min = str('min-'+product)
        max = str('max-'+product)
        min_value = int(request.form[min])
        max_value = int(request.form[max])
        product_bounds.append((min_value, max_value))
    milk_quantity = request.form['milk_quantity']
    fat_percentage = request.form['fat_percentage']
    if milk_quantity and fat_percentage:
        milk_quantity = float(milk_quantity)
        fat_percentage = float(fat_percentage)
        skimmed_milk_price = 57 * fat_percentage
        fat_price = 40
        import get_products
        import production_cost
        import skimming
        import matrix
        skimmed_milk_quantity, fat_quantity = skimming.calculate_milk_and_fat_quantity(milk_quantity, fat_percentage)
        products_list = get_products.get_products(skimmed_milk_price, fat_price)
        matrix = matrix.matrix(products_list, skimmed_milk_quantity, fat_quantity, product_bounds)
        return render_template('matrix.html', result=matrix)
    else:
        return f"Տվյալները մուտքագրված չեն։</br><a href='/calculate'><button>Վերադառնալ հավվիչ</button></a>"

@app.route('/productslist')
def productslist():
    products_list = []
    products_dir = "products"
    products = os.listdir(products_dir)
    products = [product for product in products if os.path.isdir(products_dir+'/'+product)]
    for product in products:
        ingridients = open(products_dir+'/'+product+'/ingridients', 'r').read()
        container = open(products_dir+'/'+product+'/container', 'r').read()
        selling_price = float(open(products_dir+'/'+product+'/selling_price', 'r').read())
        skimmed_milk_quantity, fat_quantity = [float(element) for element in ingridients.split(',')]
        size, container_price = [float(element) for element in container.split(',')]
        fat_quantity = float(fat_quantity) * 100
        products_list.append([product, skimmed_milk_quantity, fat_quantity, size, container_price, selling_price])
    return render_template('productslist.html', products=products_list)

@app.route('/newproduct')
def newproduct():
    return render_template('newproduct.html')

@app.route('/addproduct', methods=['POST'])
def handle_form_submission():
    error = None
    product = request.form['product']
    skimmed_milk_quantity = request.form['skimmed_milk_quantity']
    fat_quantity = request.form['fat_quantity']
    size = request.form['size']
    container_price = request.form['container_price']
    selling_price = request.form['selling_price']
    fat_quantity = float(fat_quantity) / 100
    fat_quantity = str(fat_quantity)
    if product and skimmed_milk_quantity and fat_quantity and size and container_price and selling_price:
        product = product
        parent_dir = "products"
        path = os.path.join(parent_dir, product)
        try:
            os.makedirs(path)
            with open(path + "/" + 'container', 'w') as f:
                f.write(size + ',' + container_price)
            with open(path + "/" + 'ingridients', 'w') as f:
                f.write(skimmed_milk_quantity + ',' + fat_quantity)
            with open(path + "/" + 'selling_price', 'w') as f:
                f.write(selling_price)
        except:
            error = "Նման անվանումով ապռաքատեսակ գրանցված է։"
    products_list = []
    products_dir = "products"
    products = os.listdir(products_dir)
    products = [product for product in products if os.path.isdir(products_dir+'/'+product)]
    for product in products:
        ingridients = open(products_dir+'/'+product+'/ingridients', 'r').read()
        container = open(products_dir+'/'+product+'/container', 'r').read()
        selling_price = float(open(products_dir+'/'+product+'/selling_price', 'r').read())
        skimmed_milk_quantity, fat_quantity = [float(element) for element in ingridients.split(',')]
        size, container_price = [float(element) for element in container.split(',')]
        fat_quantity = float(fat_quantity) * 100
        products_list.append([product, skimmed_milk_quantity, fat_quantity, size, container_price, selling_price])
    if error is not None:
        return render_template('newproduct.html', er=error)
    else:
        return render_template('productslist.html', products=products_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
