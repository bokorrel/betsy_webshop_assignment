from peewee import *

db = SqliteDatabase('betsy.db')

class Address(Model):
    street = CharField(null=False)
    house_number = IntegerField(null=False)
    postal_code = CharField(null=False, max_length=6)
    city = CharField(null=False)

    class Meta:
        database = db

class User(Model): #name, address data, and billing information
    name = CharField(null=False)
    address = ForeignKeyField(Address)
    billing_address = ForeignKeyField(Address)
    
    class Meta:
        database = db 

class Product(Model):  # products must have a name, a description, a price per unit, and a quantity describing the amount in stock.
    name = CharField(null=False, unique = True) 
    description = CharField(null=False)
    #tags = ValuesList(unique = True) # The tags should not be duplicated.
    price_per_unit = DecimalField(decimal_places=2) # The price should be stored in a safe way; rounding errors should be impossible.
    quantity_in_stock = IntegerField(null=False)
    owner = ForeignKeyField(User, null=True) # Each user must be able to own a number of products.
    
    class Meta:
        database = db 

#CharField(null=False, unique = True) # The tags should not be duplicated.
class Tag(Model):  
    name = CharField(null=False, unique = True) 

    class Meta:
        database = db 

class TagProduct(Model):
    tag = ForeignKeyField(Tag)
    product = ForeignKeyField(Product)

    class Meta:
        database = db 

# We want to be able to track the purchases made on the marketplace, therefore a transaction model must exist
# You can assume that only users can purchase goods
# The transaction model must link a buyer with a purchased product and a quantity of purchased items

# class Transaction(Model): #Transaction is a reserved word in SQL
class Product_Transaction(Model):
    buyer = ForeignKeyField(User)
    product = ForeignKeyField(Product)
    quantity = IntegerField(null=False)

    class Meta:
        database = db