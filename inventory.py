from db_connection import product_collection, customer_collection, premium_customer_collection, sale_collection


class Customer():
  def __init__(self,id,name,mobile_no):
    self.id=id
    self.name=name
    self.mobile_no=mobile_no
  def get_name(self):
    return self.name
  def get_mobileno(self):
    return self.mobile_no
  def set_name(self,name):
    self.name=name
  def set_mobileno(self,mobile_no):
    self.mobile_no=mobile_no

class PremiumCustomer(Customer):
  def __init__(self,id,name,mobile_no,membership_id,points):
    super().__init__(id,name,mobile_no)
    self.membership_id=membership_id
    self.points=points
  def get_points(self):
    return self.points
  def get_membership_id(self):
    return self.membership_id
  def set_points(self,points):
    self.points=points
  def set_membership_id(self,membership_id):
    self.membership_id=membership_id
  def update_points(self,points):
    self.points+=points
  def redeem_points(self,points):
    if self.points>=points:
       self.points-=points
       return points
    else:
      return 0

class Product():
  def __init__(self,id,name,qty,price,mrp_price,purchase_price):
    self.id=id
    self.name=name
    self.qty=qty
    self.price=price
    self.mrp_price=mrp_price
    self.purchase_price=purchase_price
  def get_name(self):
    return self.name
  def get_qty(self):
    return self.qty
  def get_price(self):
    return self.price
  def get_mrp_price(self):
    return self.mrp_price
  def get_purchase_price(self):
    return self.purchase_price
  def set_name(self,name):
    self.name=name
  def set_qty(self,qty):
    self.qty=qty
  def set_price(self,price):
    self.price=price
  def set_mrp_price(self,mrp_price):
    self.mrp_price=mrp_price
  def set_purchase_price(self,purchase_price):
    self.purchase_price=purchase_price
  def update_qty(self,qty,transaction_type):
    if transaction_type=='purchase':
      self.qty+=qty
    elif transaction_type=='sale':
      self.qty-=qty
  def check_availability(self,qty):
    if self.qty>=qty:
      return True
    else:
      return False
  def get_savings(self,qty):
    return (self.mrp_price-self.purchase_price)*qty
  def get_profit(self,qty):
    return (self.price-self.mrp_price)*qty

class Sale():
  def __init__(self,id,date,total_amount,total_tax,total_net_amount,total_savings,Customer,points,redeem_amount):
    self.id=id
    self.date=date
    self.total_amount=total_amount
    self.total_tax=total_tax
    self.total_net_amount=total_net_amount
    self.total_savings=total_savings
    self.Customer=Customer
    self.points=points
    self.redeem_amount=0
    self.sale_detail=[]
  def get_id(self):
    return self.id
  def get_date(self):
    return self.date
  def get_total_amount(self):
    return self.total_amount
  def get_total_tax(self):
    return self.total_tax
  def get_total_net_amount(self):
    return self.total_net_amount
  def get_total_savings(self):
    return self.total_savings
  def get_Customer(self):
    return self.Customer
  def get_points(self):
    return self.points
  def get_redeem_amount(self):
    return self.redeem_amount
  def set_id(self,id):
    self.id=id
  def set_date(self,date):
    self.date=date
  def set_total_amount(self,total_amount):
    self.total_amount=total_amount
  def set_total_tax(self,total_tax):
    self.total_tax=total_tax
  def set_total_net_amount(self,total_net_amount):
    self.total_net_amount=total_net_amount
  def set_total_savings(self,total_savings):
    self.total_savings=total_savings
  def set_Customer(self,Customer):
    self.Customer=Customer
  def set_points(self,points):
    self.points=points
  def set_redeem_amount(self,redeem_amount):
    self.redeem_amount=redeem_amount
  def update_total_amount(self,total_amount):
    self.total_amount+=total_amount
  def update_tax_amount(self):
    tax_rate = 0.18
    tax_amount = self.total_amount * tax_rate
    self.total_tax = tax_amount
    self.total_net_amount = self.total_amount + self.total_tax
  def update_net_amount(self,net_amount):
    self.total_net_amount+=net_amount
  def update_savings(self,savings):
    self.total_savings+=savings
  def finalize_bill(self):
    self.update_tax_amount()
    if isinstance(self.Customer,PremiumCustomer):
      earned_points=int(self.total_net_amount//100)
      self.Customer.update_points(earned_points)
      print(f"Points earned: {earned_points}")
    else:
      print("No points update for regular customer.")
  def redeem_points(self,points):
    if isinstance(self.Customer,PremiumCustomer):
      redeem_amount=self.Customer.redeem_points(points)
      if redeem_amount>0:
        self.redeem_amount+=redeem_amount
        self.total_net_amount-=redeem_amount
      else:
        print("Insufficient points.")
    else:
      print("No points to redeem for regular customer.")

class Sale_Detail():
    def create_sale_detail(self, sale, product, qty):
        self.sale = sale
        self.product = product
        self.qty = qty
        self.amount = qty * product.get_price()
        self.savings = product.get_savings(qty)
        sale.update_total_amount(self.amount)
        sale.update_savings(self.savings)
        product.update_qty(qty, 'sale')
        sale.sale_detail.append(self)

products={}
customers={}
premium_customers={}

def add_product():
    p_id = input("Enter product ID: ")
    name = input("Enter product name: ")
    qty = int(input("Enter product quantity: "))
    price = float(input("Enter selling price: "))
    mrp_price = float(input("Enter product MRP price: "))
    purchase_price = float(input("Enter product purchase price: "))

    product_data = {
        "_id": p_id,
        "name": name,
        "qty": qty,
        "price": price,
        "mrp_price": mrp_price,
        "purchase_price": purchase_price
    }

    product_collection.insert_one(product_data)
    print("✅ Product added to MongoDB.")


def add_stock():
    p_id = input("Enter product ID: ")
    product = product_collection.find_one({"_id": p_id})
    if product:
        qty = int(input("Enter quantity to add: "))
        new_qty = product["qty"] + qty
        product_collection.update_one({"_id": p_id}, {"$set": {"qty": new_qty}})
        print("✅ Stock updated in MongoDB.")
    else:
        print("❌ Product not found.")


import datetime

def selling():
    customer_id = input("Enter customer ID: ")
    
    customer = customer_collection.find_one({"_id": customer_id})
    premium_customer = premium_customer_collection.find_one({"_id": customer_id})

    if customer:
        is_premium = False
    elif premium_customer:
        is_premium = True
        customer = premium_customer
    else:
        print("❌ Customer not found.")
        return

    sale_details = []
    total_amount = 0
    total_savings = 0

    while True:
        p_id = input("Enter Product ID to sell (or 'done' to finish): ")
        if p_id.lower() == 'done':
            break

        product = product_collection.find_one({"_id": p_id})
        if not product:
            print("❌ Product not found.")
            continue

        qty = int(input("Enter quantity: "))
        if product["qty"] < qty:
            print("❌ Not enough stock.")
            continue

        price = product["price"]
        savings = (product["mrp_price"] - product["purchase_price"]) * qty
        amount = price * qty
        total_amount += amount
        total_savings += savings

        product_collection.update_one({"_id": p_id}, {"$inc": {"qty": -qty}})

        sale_details.append({
            "product_id": p_id,
            "product_name": product["name"],
            "qty": qty,
            "price": price,
            "amount": amount,
            "savings": savings
        })

    tax_rate = 0.18
    total_tax = total_amount * tax_rate
    total_net_amount = total_amount + total_tax
    redeem_points = 0
    redeem_amount = 0

    if is_premium:
        redeem_points = int(input("Enter points to redeem (or 0 to skip): "))
        if customer["points"] >= redeem_points:
            redeem_amount = redeem_points
            total_net_amount -= redeem_amount
            new_points = customer["points"] - redeem_points
            premium_customer_collection.update_one(
                {"_id": customer_id},
                {"$set": {"points": new_points}}
            )
        else:
            print("❌ Insufficient points.")

    points_earned = int(total_net_amount // 100)
    if is_premium:
        premium_customer_collection.update_one(
            {"_id": customer_id},
            {"$inc": {"points": points_earned}}
        )
        print(f"✅ {points_earned} points earned and updated.")

    sale_data = {
        "customer_id": customer_id,
        "is_premium": is_premium,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_amount": total_amount,
        "total_tax": total_tax,
        "total_net_amount": total_net_amount,
        "total_savings": total_savings,
        "redeem_points": redeem_points,
        "redeem_amount": redeem_amount,
        "points_earned": points_earned,
        "sale_details": sale_details
    }

    sale_collection.insert_one(sale_data)

    print("\n✅ Sale completed.")
    print(f"Total amount: {total_amount}")
    print(f"Total tax: {total_tax}")
    print(f"Total net amount: {total_net_amount}")
    print(f"Total savings: {total_savings}")
    print(f"Points earned: {points_earned}")



def add_customer():
    cid = input("Enter Customer ID: ")
    name = input("Enter Name: ")
    mobile = input("Enter Mobile No: ")
    customer = {"_id": cid, "name": name, "mobile": mobile}
    customer_collection.insert_one(customer)
    print("✅ Customer added.")

def add_premium_customer():
    cid = input("Enter Customer ID: ")
    name = input("Enter Name: ")
    mobile = input("Enter Mobile No: ")
    mid = input("Enter Membership ID: ")
    points = int(input("Enter Starting Points: "))
    customer = {
        "_id": cid,
        "name": name,
        "mobile": mobile,
        "membership_id": mid,
        "points": points
    }
    premium_customer_collection.insert_one(customer)
    print("✅ Premium Customer added.")

def main_menu():
    while True:
        print("\n--- Inventory System ---")
        print("1. Add Product")
        print("2. Add Stock")
        print("3. Selling")
        print("4. Add Customer")
        print("5. Add Premium Customer")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_product()
        elif choice == '2':
            add_stock()
        elif choice == '3':
            selling()
        elif choice == '4':
            add_customer()
        elif choice == '5':
            add_premium_customer()
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()