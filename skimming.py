def calculate_milk_and_fat_quantity(milk_quantity, fat_percentage):

  fat_quantity = milk_quantity * fat_percentage / 100
  skimmed_milk_quantity = milk_quantity - fat_quantity
  
  #print("Զտված կաթի ծավալ:", skimmed_milk_quantity, "լիտր")
  #print("Յուղի ծավալ:", fat_quantity, "լիտր")
  
  return skimmed_milk_quantity, fat_quantity
