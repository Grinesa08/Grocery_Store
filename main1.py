# Import necessary libraries
import streamlit as st
import sqlite3

# Create connection to SQLite database
conn = sqlite3.connect('grocery_store.db')
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS Product
             (name text, quantity integer, place text)''')
c.execute('''CREATE TABLE IF NOT EXISTS Orders
             (product_name text, quantity integer, date text)''')


# Define CRUD operations
def add_product(name, quantity, place):
    c.execute("INSERT INTO Product VALUES (?, ?, ?)", (name, quantity, place))
    conn.commit()

def update_product_quantity(name, quantity):
    c.execute("UPDATE Product SET quantity = ? WHERE name = ?", (quantity, name))
    conn.commit()

def delete_product(name):
    c.execute("DELETE FROM Product WHERE name = ?", (name,))
    conn.commit()

def add_order(product_name, quantity, date):
    # check if the product exists
    c.execute("SELECT quantity FROM Product WHERE name = ?", (product_name,))
    result = c.fetchone()
    if result is None:
        st.error(f"{product_name} does not exist in the Product table.")
        return
    available_quantity = result[0]
    # check if the quantity ordered is available
    if quantity > available_quantity:
        st.error(f"Only {available_quantity} {product_name} available in the Product table.")
        return
    c.execute("INSERT INTO Orders VALUES (?, ?, ?)", (product_name, quantity, date))
    conn.commit()
    # Reduce the quantity of the product in the Product table
    new_quantity = available_quantity - quantity
    c.execute("UPDATE Product SET quantity = ? WHERE name = ?", (new_quantity, product_name))
    conn.commit()
    st.success("Order added successfully")

def update_order_quantity(product_name, quantity):
    c.execute("UPDATE Orders SET quantity = ? WHERE product_name = ?", (quantity, product_name))
    conn.commit()

def delete_order(product_name):
    # get the quantity of the product that has been removed from the Orders table
    c.execute("SELECT quantity FROM Orders WHERE product_name = ?", (product_name,))
    result = c.fetchone()
    if result is None:
        st.error(f"No orders found for {product_name}.")
        return
    removed_quantity = result[0]
    # increment the quantity of the product in the Product table
    c.execute("UPDATE Product SET quantity = quantity + ? WHERE name = ?", (removed_quantity, product_name))
    conn.commit()
    c.execute("DELETE FROM Orders WHERE product_name = ?", (product_name,))
    conn.commit()
    st.success("Order deleted successfully")

# Define Streamlit web interface
def main():
    st.title("Grocery Store Application")
    menu = ["Add Product", "Update Product Quantity", "Delete Product", "Add Order", "Update Order Quantity", "Delete Order"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Add Product":
        st.subheader("Add Product")
        name = st.text_input("Name of product")
        quantity = st.number_input("Quantity", min_value=0)
        place = st.selectbox("Place", ["Prishtine", "Ferizaj", "Prizren", "Peje", "Gjakove", "Gjilan"])
        if st.button("Add"):
            add_product(name, quantity, place)
            st.success("Product added successfully")
            name = ""
            quantity = 0

    elif choice == "Update Product Quantity":
        st.subheader("Update Product Quantity")
        name = st.text_input("Name of product")
        quantity = st.number_input("Quantity", min_value=0)
        if st.button("Update"):
            update_product_quantity(name, quantity)
            st.success("Product quantity updated successfully")
            name = ""
            quantity = 0

    elif choice == "Delete Product":
        st.subheader("Delete Product")
        name = st.text_input("Name of product")
        if st.button("Delete"):
            delete_product(name)
            st.success("Product deleted successfully")
            name = ""

    elif choice == "Add Order":
        st.subheader("Add Order")
        product_name = st.text_input("Name of product")
        quantity = st.number_input("Quantity", min_value=0)
        date = st.date_input("Date")
        if st.button("Add"):
             if add_order(product_name, quantity, date):
                st.success("Order added successfully")
                product_name = ""
                quantity = 0

    elif choice == "Update Order Quantity":
        st.subheader("Update Order Quantity")
        product_name = st.text_input("Name of product")
        quantity = st.number_input("Quantity", min_value=0)
        if st.button("Update"):
            update_order_quantity(product_name, quantity)
            st.success("Order quantity updated successfully")
            product_name = ""
            quantity = 0

    elif choice == "Delete Order":
        st.subheader("Delete Order")
        product_name = st.text_input("Name of product")
        if st.button("Delete"):
            delete_order(product_name)
            st.success("Order deleted successfully")
            product_name = ""

if __name__ == '__main__':
    main()
