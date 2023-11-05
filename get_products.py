import os
import production_cost

def get_products(skimmed_milk_price, fat_price):

  headers = ['Ապռանքի անվանում․', 'Բաղադրություն \n 1 լ/կգ համար․ զտած կաթ \n (լիտր)', 'Բաղադրություն \n 1 լ/կգ համար յուղ \n (%)', 'Տարաի չափը \n (կգ/լիտր)', 'Տարաի գինը \n (դրամ)', 'Արտադրության գին \n (դրամ)', 'Վաճառքի գին \n (դրամ)', 'Շահույթ 1 \n ապռանքի համար \n (դրամ)']
  data = []
  products_list = []
  products_dir = "work" 
 
  products = os.listdir(products_dir)
  products = [product for product in products if os.path.isdir(products_dir+'/'+product)]

  for product in products:
    ingridients = open(products_dir+'/'+product+'/ingridients', 'r').read()
    selling_price = float(open(products_dir+'/'+product+'/selling_price', 'r').read())
    container = open(products_dir+'/'+product+'/container', 'r').read()
    skimmed_milk_quantity, fat_quantity = [float(element) for element in ingridients.split(',')]
    size, container_price = [float(element) for element in container.split(',')]
    cost = production_cost.production_cost(skimmed_milk_quantity, fat_quantity, skimmed_milk_price, fat_price, container_price, size)
    margin = selling_price - cost
    result = [product, skimmed_milk_quantity, fat_quantity * 100, size, container_price, cost, selling_price, margin]
    products_list.append([product, skimmed_milk_quantity, fat_quantity, size, container_price, round(cost, 2), selling_price, round(margin, 2)])
    data.append(result)
  

  #print(table)
  
  return products_list