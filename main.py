__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

#import models 
from models import *
import random

# random test data
tables = [Address, User, Tag, Product, TagProduct, Product_Transaction]
test_streets = ['kerkstraat','hoofdstraat','landweg']
test_house_numbers = range(1,300)
test_postal_codes = ['1938AI','3048KE','2840LD','3974IE','2083WK','9532TR']
test_cities = ['Utrecht','Amsterdam','Rotterdam','Maastricht','Groningen']
test_user_names = ['bob','alice','maria','paul','frank','roos']
test_tags = ['furniture','wood','metalic','garden','clothing','wool','sustainable','vintage']
test_product_names = ['chair Lulu','industrial lamp Kiki','fire pit Ed','modern painting Lisa','lounge set Ludo','bamboo plates','moody mugs','stainless pan set', 'egg chair']
#test_prices = random.uniform(5.00,200.00) #range(5.00,200.00)
test_quantities = range(0,500)

def search(term):
    # Search for products based on a term. 
    # Searching for 'sweater' should yield all products that have the word 'sweater' in the name. 
    # This search should be case-insensitive    
    # Bonus: The search should target both the name and description fields.
    matching_products = []
    query = (Product
             .select()
             .where(Product.name.contains(term.lower()) 
                    or Product.name.contains(term.upper()) 
                    or Product.description.contains(term.lower()) 
                    or Product.description.contains(term.upper()) 
                    )
            )
    for product in query:
        # add to list
        matching_products.append(product)
    return matching_products

def list_user_products(user_id):
    # View the products of a given user
    user_products = []
    query = (Product
             .select()
             .where(Product.owner == user_id)
            )
    for product in query:
        # add to list
        user_products.append(product)
    return user_products

def list_products_per_tag(tag_id):
    tag_products = []
    query = (TagProduct
             .select()
             .where(TagProduct.tag==tag_id)
             .join(Tag, on=(Tag.id == TagProduct.tag))
             .join(Product, on=(Product.id == TagProduct.product))
            )
    for tag_product in query:
        product = tag_product.product 
        # add to list
        tag_products.append(product)
    return tag_products

def add_product_to_catalog(user_id, product):
    # get existing product
    my_product = Product(id=product)
    # update owner
    my_product.owner = user_id    
    my_product.save()
    return

def update_stock(product_id, new_quantity):
    # get existing product
    my_product = Product(id=product_id)
    # update quantity
    my_product.quantity_in_stock = new_quantity
    my_product.save()
    return

def purchase_product(product_id, buyer_id, quantity):
    # create new Transaction record
    Product_Transaction.create(buyer=buyer_id, product=product_id, quantity=quantity)
    return

def remove_product(product_id):  # Remove a product from a user
    # get existing product
    my_product = Product(id=product_id)
    # remove owner
    my_product.owner = None
    my_product.save()
    return

def populate_test_database(): # Add a populate_test_database function that fills the database with example data that works with your queries
    # first create clean tables 
    db.drop_tables(tables)
    db.create_tables(tables)

    # add 10 random addresses
    address_records = []
    for x in range(1,10):
        new_address = Address.create( street=random.choice(test_streets)
                                    , house_number=random.choice(test_house_numbers)
                                    , postal_code=random.choice(test_postal_codes)
                                    , city=random.choice(test_cities))
        new_address.save()
        address_records.append(new_address)
        
    # add users
    user_records = []
    for user_name in test_user_names:
        new_user = User.create(name=user_name, address=random.choice(address_records), billing_address=random.choice(address_records))
        new_user.save()
        user_records.append(new_user)

    # add tags
    tag_records = []
    for tag in test_tags:
        new_tag = Tag.create(name=tag)
        new_tag.save()
        tag_records.append(new_tag)

    # add products
    product_records = []
    for product in test_product_names:
        new_product = Product.create(name=product
                                     ,description=f"'{product}' is one of our high-class products. Avaliable now!"
                                     ,price_per_unit=round(random.uniform(5.00,200.00),2)
                                     ,quantity_in_stock=random.choice(test_quantities)
                                     ,owner=random.choice(user_records)
                                    )
        new_product.save()                             
        product_records.append(new_product)

    # add 20 random tags to products
    for x in range(1,20):
        new_product_tag = TagProduct.create(tag=random.choice(tag_records),product=random.choice(product_records))
        new_product_tag.save()

# create test data
populate_test_database()

# ENABLE TESTS BELOW IF NEEDED
""" 
# get all products that contain 'chair' in the name
print('search result for chair=', search('Chair') )  # should return 2 products

# get all products owned by user
user_name = random.choice(test_user_names)
print("products owned by user",user_name,":", list_user_products( User.get(name=user_name) ))

# get all products with the 'vintage' tag
tag = random.choice(test_tags)
print("search result for tag",tag,"=", list_products_per_tag( Tag.get(name=tag) ))

# add product to user
user_name = random.choice(test_user_names)
product_name = random.choice(test_product_names)
if add_product_to_catalog(User.get(name=user_name), Product.get(name=product_name)) == None:
    print("product",product_name,"added to user", user_name )

# remove product from user
product_name = random.choice(test_product_names)
if remove_product(Product.get(name=product_name)) == None:
    print("owner removed from product",product_name)

# update stock
product_name = random.choice(test_product_names)
quantity = random.choice(test_quantities)
if update_stock(Product.get(name=product_name), quantity) == None:
    print("stock for product",product_name,"updated to", quantity )

# purchase
product_name = random.choice(test_product_names)
user_name = random.choice(test_user_names)
quantity = random.choice(test_quantities)
if purchase_product(Product.get(name=product_name), User.get(name=user_name),quantity) == None:
    print(quantity,"x",product_name,"purchased by", user_name) """