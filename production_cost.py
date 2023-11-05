def production_cost(skimmed_milk_quantity, fat_quantity, skimmed_milk_price, fat_price, container_price, size):
  production_cost = (((skimmed_milk_quantity * skimmed_milk_price) + (fat_quantity * fat_price)) * size) + container_price
  return production_cost