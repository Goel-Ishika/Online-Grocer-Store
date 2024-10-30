This project is a simple online grocery store management application built using Streamlit to demonstrate CRUD operations on a MySQL database. The application provides two main interfaces: one for users and one for admins.

Features

User Functionality

Signup/Login: Users can sign up by providing their name and phone number, which are used as their credentials for logging in.
Product Browsing: Users can view available products along with their prices and stock information.
Add to Cart: Users can add products to their cart, specifying the quantity for each item.
Checkout: Users can proceed to checkout, where the order is processed, and the cart is cleared after a successful purchase.
Unique Cart Management: A unique cart is automatically created for each user upon signup/login, ensuring seamless order management. The cart is cleared and de-linked after each checkout.
Admin Functionality

Admin Login: Admins can log in using a predefined username and password.
Manage Inventory: Admins can view the entire inventory of available products and manage stock levels.
View Orders: Admins can view all orders placed by users, including customer details and order amounts.
Technology Stack

Frontend: Streamlit, a Python-based web application framework.
Backend: MySQL database for storing products, users, carts, orders, and admin data.
PDF Generation: FPDF for generating invoices (if required).
How to Run the Application

Clone the Repository: Clone this repository to your local machine.
Install Requirements: Install required packages using the command:
pip install -r requirements.txt
Set Up the Database: Create the MySQL database using the provided SQL script (database_setup.sql). Ensure that the MySQL server is running and accessible.
Configure Database Connection: Modify db_connection.py to include your database connection settings.
Run the Application: Launch the Streamlit app using the command: streamlit run app.py
Usage

User Interface: After launching the application, users can choose to either sign up as a new user or log in as an existing user to access the grocery store features.
Admin Interface: Admins can manage products and view all orders by logging in using their admin credentials.
Database Schema The MySQL database includes the following tables:

Categories: Stores product categories.
Suppliers: Stores supplier information.
Products : Stores details of products available in the store.
Customers : Stores customer information.
Admins : Stores admin credentials for managing the store.
Carts : Stores cart information for each user.
Cart_Items : Stores items added to each cart.
Orders : Stores completed orders.
Order_Items: Stores details of items included in each order.
Future Improvements

Authentication Security: Implement password hashing for enhanced security.
Real-Time Stock Updates: Update product stock in real-time as users add items to their cart.
Enhanced User Experience: Improve UI design and include better user feedback during operations.
License This project is open-source and available under the MIT License.

Feel free to contribute to the project or suggest improvements!

Contact For any queries or support, please reach out to the project maintainers.
