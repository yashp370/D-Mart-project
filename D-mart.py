import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mysq001"
)

cursor = db.cursor()

# Admin 
def admin_login():
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")

    cursor.execute("SELECT * FROM admin01 WHERE email = %s AND password = %s", (email, password))
    admin = cursor.fetchone()

    if admin:
        print("Login successful!")
        return True
    else:
        print("Invalid email or password!")
        return False


def add_customer(name, email, phone):
    query = "INSERT INTO customer (name, email, phone) VALUES (%s, %s, %s)"
    values = (name, email, phone)
    cursor.execute(query, values)
    db.commit()
    print(f"Customer '{name}' added successfully.")

# View customers
def view_customers():
    cursor.execute("SELECT * FROM customer")
    customers = cursor.fetchall()
    
    print("Customer List:")
    print(f"{'customer_id':<5} | {'Name':<10} | {'Email':<25} | {'Phone':<35}")
    print("-" * 90)
    for customer in customers:
        print(f"{customer[0]:<10} | {customer[1]:<15} | {customer[2]:<30} | {customer[3]:<45}")

# Add new item
def add_item(name, category, price, stock):
    query = "INSERT INTO item (name, category, price, stock) VALUES (%s, %s, %s, %s)"
    values = (name, category, price, stock)
    cursor.execute(query, values)
    db.commit()
    print(f"Item '{name}' added successfully.")

# View  items
def view_items():
    cursor.execute("SELECT * FROM item")
    items = cursor.fetchall()
    
    print("Item List:")
    print("ID , Name , Category , Price , Stock")
    for item in items:
        print(f"{item[0]} , {item[1]} , {item[2]} , {item[3]} , {item[4]}")

# Place order
def place_order(customer_id, item_id, quantity):
    cursor.execute("SELECT stock FROM item WHERE item_id = %s", (item_id,))
    item = cursor.fetchone()
    
    if item and item[0] >= quantity:
        query = "INSERT INTO booked (customer_id, item_id, quantity) VALUES (%s, %s, %s)"
        values = (customer_id, item_id, quantity)
        cursor.execute(query, values)
        cursor.execute("UPDATE item SET stock = stock - %s WHERE item_id = %s", (quantity, item_id))
        db.commit()
        print("Order placed successfully.")
    else:
        print("Insufficient stock or item not available.")

# View  orders
def view_orders():
    query = """
    SELECT customer.name, item.name, booked.quantity, booked.booking_date
    FROM booked
    JOIN customer ON booked.customer_id = customer.customer_id
    JOIN item ON booked.item_id = item.item_id
    """
    cursor.execute(query)
    orders = cursor.fetchall()
    
    print("Order List:")
    print("Customer Name , Item Name , Quantity , Booking Date")
    for order in orders:
        print(f"{order[0]} , {order[1]} , {order[2]} , {order[3]}")

# Main Menu
def menu():
    if not admin_login():
        return

    while True:
        print("\n Store Management System")
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Add Item")
        print("4. View Items")
        print("5. Place Order")
        print("6. View Orders")
        print("7. Exit")

        i = int(input("Enter choice: "))

        if i == 1:
            name = input("Enter customer name: ")
            email = input("Enter customer email: ")
            phone = input("Enter customer phone: ")
            
            (name, email, phone)

        elif i == 2:
            
            view_customers()
            

        elif i == 3:
            name = input("Enter item name: ")
            category = input("Enter item category: ")
            price = float(input("Enter item price: "))
            stock = int(input("Enter item stock: "))
            add_item(name, category, price, stock)

        elif i == 4:
            view_items()

        elif i == 5:
            customer_id = int(input("Enter customer ID: "))
            item_id = int(input("Enter item ID: "))
            quantity = int(input("Enter quantity: "))
            place_order(customer_id, item_id, quantity)

        elif i == 6:
            view_orders()

        elif i == 7:
            print("Thank you for using the store management system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()

# Close the cursor and database connection
cursor.close()
db.close()