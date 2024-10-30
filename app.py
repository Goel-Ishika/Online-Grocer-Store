import streamlit as st
from db_connection import execute_read_query, execute_write_query, test_connection
from fpdf import FPDF
import pandas as pd
from datetime import datetime
import time

st.title("Online Grocery Store Management")
st.write("Demonstration of MySQL Operations")

# Check if the connection to the database is successful
if not test_connection():
    st.error("Unable to connect to the database. Please check the connection settings.")
    st.stop()  # Stop further execution if the database connection fails

# Initialize session state if not already set
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False
    st.session_state.role = None
    st.session_state.customer_id = None

# Variable to control login status
is_authenticated = st.session_state.is_authenticated
role = st.session_state.role

# User or Admin selection
if not is_authenticated:
    role = st.selectbox("Login As:", ["Select", "User", "Admin"])

# User Login and Signup Section
if not is_authenticated and role == "User":
    user_action = st.radio("Are you a new user or returning?", ["New User", "Returning User"])

    if user_action == "New User":
        st.header("User Signup")
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")

        if st.button("Signup"):
            # Use name as username and phone as password
            signup_query = """
            INSERT INTO Customers (FirstName, Phone, Username, Password)
            VALUES (%s, %s, %s, %s)
            """
            # Insert new customer
            try:
                insert_success = execute_write_query(signup_query, (name, phone, name, phone))

                if insert_success:
                    # Retry fetching customer information after signup
                    retries = 3
                    customer = None
                    while retries > 0:
                        customer_id_query = "SELECT CustomerID FROM Customers WHERE Phone = %s"
                        customer = execute_read_query(customer_id_query, (phone,))
                        if customer is not None and not customer.empty:
                            break
                        time.sleep(0.1)  # Short delay before retrying
                        retries -= 1

                    if customer is not None and not customer.empty:
                        customer_id = int(customer['CustomerID'][0])

                        # Automatically create a cart for this new customer
                        create_cart_query = "INSERT INTO Carts (CustomerID) VALUES (%s)"
                        execute_write_query(create_cart_query, (customer_id,))
                        
                        # Log the user in automatically
                        st.session_state.is_authenticated = True
                        st.session_state.role = "User"
                        st.session_state.customer_id = customer_id
                        
                        st.success("Signup successful. You have been logged in automatically.")
                    else:
                        st.error("Signup successful, but could not fetch customer details. Please try logging in.")
                else:
                    st.error("Signup failed due to database issue.")
            except Exception as e:
                st.error(f"Signup failed: {e}")

    elif user_action == "Returning User":
        st.header("User Login")
        user_name = st.text_input("Enter your name")
        user_phone = st.text_input("Enter your phone number")

        if st.button("Login as User"):
            user_query = "SELECT * FROM Customers WHERE FirstName = %s AND Phone = %s"
            user = execute_read_query(user_query, (user_name, user_phone))

            if user is not None and not user.empty:
                st.success(f"Welcome {user_name}!")
                st.session_state.is_authenticated = True
                st.session_state.role = "User"
                st.session_state.customer_id = int(user['CustomerID'][0])  # Storing customer ID in session state
            else:
                st.error("Invalid Name or Phone Number.")

# Admin Login Section
elif not is_authenticated and role == "Admin":
    st.header("Admin Login")
    admin_username = st.text_input("Enter Admin Username")
    admin_password = st.text_input("Enter Admin Password", type="password")

    if st.button("Login as Admin"):
        admin_query = "SELECT * FROM Admins WHERE Username = %s AND Password = %s"
        admin = execute_read_query(admin_query, (admin_username, admin_password))

        if admin is not None and not admin.empty:
            st.success("Admin Login Successful!")
            st.session_state.is_authenticated = True
            st.session_state.role = "Admin"
        else:
            st.error("Incorrect Username or Password.")

# If authenticated, skip login page and show the rest of the functionality
if st.session_state.is_authenticated and st.session_state.role == "User":
    customer_id = st.session_state.customer_id  # Ensure customer_id is always retrieved from session state
    st.header("User - Shop Groceries")

    # View Inventory for Users
    st.subheader("Available Inventory")
    inventory_query = "SELECT ProductName, Price, Stock FROM Products WHERE Stock > 0"
    inventory = execute_read_query(inventory_query)
    if inventory is not None and not inventory.empty:
        st.write(inventory)
    else:
        st.write("No products available currently.")

    # Product Search with Suggestive Search
    product_query = "SELECT ProductName FROM Products WHERE Stock > 0"
    product_names_result = execute_read_query(product_query)
    if product_names_result is not None and not product_names_result.empty:
        products = product_names_result['ProductName'].tolist()
    else:
        products = []

    product_name = st.selectbox("Search for a product", options=products)
    quantity = st.number_input("Quantity", min_value=1)

    if st.button("Add to Cart"):
        # Fetch Product Details
        product_details_query = "SELECT * FROM Products WHERE ProductName = %s"
        product_details = execute_read_query(product_details_query, (product_name,))
        if product_details is not None and not product_details.empty:
            product_data = product_details.iloc[0]
            product_id = int(product_data['ProductID'])  # Convert to Python int

            # Since every customer is guaranteed to have a cart, we fetch it directly
            cart_query = "SELECT CartID FROM Carts WHERE CustomerID = %s"
            cart = execute_read_query(cart_query, (customer_id,))

            if cart is not None and not cart.empty:
                cart_id = int(cart.iloc[0]['CartID'])  # Convert to Python int
                add_cart_item_query = """
                INSERT INTO Cart_Items (CartID, ProductID, Quantity) VALUES (%s, %s, %s)
                """
                execute_write_query(add_cart_item_query, (cart_id, product_id, int(quantity)))
                st.success("Added to cart successfully!")
            else:
                st.error("Could not fetch the cart. Please try again.")

    # View Cart and Checkout
    st.subheader("Your Cart")
    cart_items_query = """
    SELECT p.ProductName, ci.Quantity, p.Price, (ci.Quantity * p.Price) as Total, ci.ProductID
    FROM Cart_Items ci
    JOIN Products p ON ci.ProductID = p.ProductID
    WHERE ci.CartID = (SELECT CartID FROM Carts WHERE CustomerID = %s)
    """
    cart_items = execute_read_query(cart_items_query, (customer_id,))

    if cart_items is not None and not cart_items.empty:
        st.write(cart_items)

        if st.button("Checkout"):
            total_amount = float(cart_items['Total'].sum())
            order_query = "INSERT INTO Orders (CustomerID, OrderDate, TotalAmount) VALUES (%s, %s, %s)"
            order_date = datetime.now()

            # Insert order and commit
            execute_write_query(order_query, (customer_id, order_date, total_amount))

            # Get the latest Order ID
            order_id_query = "SELECT LAST_INSERT_ID() as OrderID"
            order_id_result = execute_read_query(order_id_query)
            if order_id_result is not None and not order_id_result.empty:
                order_id = int(order_id_result['OrderID'][0])

                # Insert Order Items and clear cart
                for _, row in cart_items.iterrows():
                    order_item_query = """
                    INSERT INTO Order_Items (OrderID, ProductID, Quantity, Price)
                    VALUES (%s, %s, %s, %s)
                    """
                    execute_write_query(order_item_query, (
                        order_id, 
                        int(row['ProductID']), 
                        int(row['Quantity']), 
                        float(row['Price'])
                    ))

                # Check if cart_id is properly defined before using it
                if 'cart_id' in locals():
                    # Clear cart
                    delete_cart_query = "DELETE FROM Cart_Items WHERE CartID = %s"
                    execute_write_query(delete_cart_query, (cart_id,))
                    st.success(f"Order #{order_id} has been placed successfully!")
                else:
                    st.error("Cart could not be found during checkout. Please try again.")
            else:
                st.error("Could not retrieve the latest Order ID. Please try again.")

if st.session_state.is_authenticated and st.session_state.role == "Admin":
    st.header("Admin - Manage Store")

    # View Complete Inventory
    st.subheader("Current Inventory")
    inventory_query = "SELECT ProductName, Price, Stock FROM Products"
    inventory = execute_read_query(inventory_query)
    if inventory is not None and not inventory.empty:
        st.write(inventory)
    else:
        st.write("No products available currently.")

    # View All Orders
    st.subheader("All Orders")
    orders_query = """
    SELECT o.OrderID, o.OrderDate, o.TotalAmount, c.FirstName, c.Phone
    FROM Orders o
    JOIN Customers c ON o.CustomerID = c.CustomerID
    """
    orders = execute_read_query(orders_query)
    if orders is not None and not orders.empty:
        st.write(orders)
    else:
        st.write("No orders have been placed yet.")
