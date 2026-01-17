import sqlite3
import os
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Production-scale configuration (Massive Dataset Upgrade)
NUM_USERS = 500
NUM_PRODUCTS = 100
NUM_ORDERS = 2000
NUM_WAREHOUSES = 20
NUM_TICKETS = 500 # Increased

def create_connection(db_name):
    db_path = os.path.join(DATA_DIR, db_name)
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    return conn

def generate_production_data():
    print(f"Generating Comprehensive Production Data ({NUM_USERS} users, {NUM_ORDERS} orders)...")
    
    # 1. Users
    users = []
    users.append((1, "Alice Johnson", "alice.j@example.com", "Yes"))
    for i in range(2, NUM_USERS + 1):
        users.append((i, fake.name(), fake.unique.email(), random.choice(["Yes", "No"])))
        
    # 2. Products
    products = []
    products.append((1, "Gaming Monitor", "Electronics", 499.99))
    product_names = ["Laptop", "Smartphone", "Headphones", "Desk Lamp", "Office Chair", "Keyboard", "Mouse", "Webcam"]
    for i in range(2, NUM_PRODUCTS + 1):
        products.append((i, f"{random.choice(['Pro', 'Ultra', 'Basic'])} {random.choice(product_names)}", "Retail", round(random.uniform(20, 1500), 2)))
        
    # 3. Warehouses
    warehouses = []
    for i in range(1, NUM_WAREHOUSES + 1):
        warehouses.append((i, fake.city(), fake.name()))
        
    # 4. Orders, Shipments, Tracking
    orders = []
    shipments = []
    tracking = []
    trk_id_counter = 1
    
    # Alice's fixed order
    orders.append((101, 1, 1, "2026-01-10", "Shipped"))
    shipments.append((5001, 101, "TRK-ALICE-101", "2026-01-20"))
    tracking.append((trk_id_counter, 5001, 1, "2026-01-11 08:00:00", "Package Picked Up"))
    trk_id_counter += 1
    tracking.append((trk_id_counter, 5001, 1, "2026-01-12 14:00:00", "In Transit - Distribution Center"))
    trk_id_counter += 1

    for i in range(2, NUM_ORDERS + 1):
        order_id = i + 101
        user_id = random.randint(1, NUM_USERS)
        prod_id = random.randint(1, NUM_PRODUCTS)
        # Higher chance of being Delivered/Shipped for 2000 orders
        status = random.choice(["Processing", "Shipped", "Delivered", "Delivered", "Shipped"])
        date = fake.date_between(start_date='-30d', end_date='today')
        orders.append((order_id, user_id, prod_id, str(date), status))
        
        if status in ["Shipped", "Delivered"]:
            shipment_id = 5000 + order_id
            trk = fake.bothify(text='TRK-##########').upper()
            shipments.append((shipment_id, order_id, trk, str(date + timedelta(days=5))))
            tracking.append((trk_id_counter, shipment_id, random.randint(1, NUM_WAREHOUSES), str(date + timedelta(days=1)), "Picked Up"))
            trk_id_counter += 1
            if status == "Delivered":
                tracking.append((trk_id_counter, shipment_id, random.randint(1, NUM_WAREHOUSES), str(date + timedelta(days=4)), "Delivered"))
            else:
                tracking.append((trk_id_counter, shipment_id, random.randint(1, NUM_WAREHOUSES), str(date + timedelta(days=2)), "In Transit"))
            trk_id_counter += 1

    # 5. PayGuard: Wallets, Transactions, PaymentMethods
    wallets = []
    transactions = []
    payment_methods = []
    tx_id_counter = 30001
    
    # Alice's wallet
    wallets.append((10001, 1, 1500.00, "USD"))
    payment_methods.append((20001, 10001, "Visa", "12/28"))
    transactions.append((tx_id_counter, 10001, 101, 499.99, "Debit"))
    tx_id_counter += 1

    for i in range(1, NUM_USERS + 1):
        if i == 1: continue # Alice already added
        wallet_id = 10000 + i
        wallets.append((wallet_id, i, round(random.uniform(100, 5000), 2), "USD"))
        payment_methods.append((20000 + i, wallet_id, random.choice(["Visa", "MasterCard", "Amex"]), "10/27"))
        
        # Add transactions for ALL orders
        for o in orders:
            if o[1] == i:
                transactions.append((tx_id_counter, wallet_id, o[0], round(random.uniform(20, 1000), 2), "Debit"))
                tx_id_counter += 1

    # 6. CareDesk: Tickets, Messages, Surveys
    tickets = []
    messages = []
    surveys = []
    msg_id_counter = 1
    srv_id_counter = 8001
    
    # Alice's ticket
    tickets.append((7001, 1, 101, "Late Delivery", "Open"))
    messages.append((msg_id_counter, 7001, "Alice Johnson", "Where is my monitor? It has been 10 days!", "2026-01-11 10:00:00"))
    msg_id_counter += 1
    messages.append((msg_id_counter, 7001, "Support Agent", "We are looking into the shipment delay at the Distribution Center.", "2026-01-11 11:30:00"))
    msg_id_counter += 1
    surveys.append((srv_id_counter, 7001, 4, "Good response, but item still missing."))
    srv_id_counter += 1

    for i in range(2, NUM_TICKETS + 1):
        ticket_id = 7000 + i
        order_obj = random.choice(orders)
        user_id = order_obj[1]
        order_ref = order_obj[0]
        issue = random.choice(["Refund", "Status", "Damaged", "Missing Item"])
        status = random.choice(["Open", "Closed", "Closed"])
        tickets.append((ticket_id, user_id, order_ref, issue, status))
        
        # Messages
        num_msgs = random.randint(1, 3)
        for _ in range(num_msgs):
            messages.append((msg_id_counter, ticket_id, random.choice(["User", "Agent", "System"]), fake.sentence(), str(datetime.now() - timedelta(hours=random.randint(1, 100)))))
            msg_id_counter += 1
        
        # Surveys for Closed tickets
        if status == "Closed":
            surveys.append((srv_id_counter, ticket_id, random.randint(1, 5), fake.sentence()))
            srv_id_counter += 1

    # --- DB POPULATION ---
    # ShopCore
    conn = create_connection("DB_ShopCore.db")
    c = conn.cursor()
    c.execute('CREATE TABLE Users (UserID INTEGER PRIMARY KEY, Name TEXT, Email TEXT, PremiumStatus TEXT)')
    c.execute('CREATE TABLE Products (ProductID INTEGER PRIMARY KEY, Name TEXT, Category TEXT, Price REAL)')
    c.execute('CREATE TABLE Orders (OrderID INTEGER PRIMARY KEY, UserID INTEGER, ProductID INTEGER, OrderDate TEXT, Status TEXT)')
    c.executemany('INSERT INTO Users VALUES (?,?,?,?)', users)
    c.executemany('INSERT INTO Products VALUES (?,?,?,?)', products)
    c.executemany('INSERT INTO Orders VALUES (?,?,?,?,?)', orders)
    conn.commit(); conn.close()
    
    # ShipStream
    conn = create_connection("DB_ShipStream.db")
    c = conn.cursor()
    c.execute('CREATE TABLE Shipments (ShipmentID INTEGER PRIMARY KEY, OrderID INTEGER, TrackingNumber TEXT, EstimatedArrival TEXT)')
    c.execute('CREATE TABLE Warehouses (WarehouseID INTEGER PRIMARY KEY, Location TEXT, ManagerName TEXT)')
    c.execute('CREATE TABLE TrackingEvents (EventID INTEGER PRIMARY KEY, ShipmentID INTEGER, WarehouseID INTEGER, Timestamp TEXT, StatusUpdate TEXT)')
    c.executemany('INSERT INTO Shipments VALUES (?,?,?,?)', shipments)
    c.executemany('INSERT INTO Warehouses VALUES (?,?,?)', warehouses)
    c.executemany('INSERT INTO TrackingEvents VALUES (?,?,?,?,?)', tracking)
    conn.commit(); conn.close()
    
    # PayGuard
    conn = create_connection("DB_PayGuard.db")
    c = conn.cursor()
    c.execute('CREATE TABLE Wallets (WalletID INTEGER PRIMARY KEY, UserID INTEGER, Balance REAL, Currency TEXT)')
    c.execute('CREATE TABLE Transactions (TransactionID INTEGER PRIMARY KEY, WalletID INTEGER, OrderID INTEGER, Amount REAL, Type TEXT)')
    c.execute('CREATE TABLE PaymentMethods (MethodID INTEGER PRIMARY KEY, WalletID INTEGER, Provider TEXT, ExpiryDate TEXT)')
    c.executemany('INSERT INTO Wallets VALUES (?,?,?,?)', wallets)
    c.executemany('INSERT INTO Transactions VALUES (?,?,?,?,?)', transactions)
    c.executemany('INSERT INTO PaymentMethods VALUES (?,?,?,?)', payment_methods)
    conn.commit(); conn.close()
    
    # CareDesk
    conn = create_connection("DB_CareDesk.db")
    c = conn.cursor()
    c.execute('CREATE TABLE Tickets (TicketID INTEGER PRIMARY KEY, UserID INTEGER, ReferenceID INTEGER, IssueType TEXT, Status TEXT)')
    c.execute('CREATE TABLE TicketMessages (MessageID INTEGER PRIMARY KEY, TicketID INTEGER, Sender TEXT, Content TEXT, Timestamp TEXT)')
    c.execute('CREATE TABLE SatisfactionSurveys (SurveyID INTEGER PRIMARY KEY, TicketID INTEGER, Rating INTEGER, Comments TEXT)')
    c.executemany('INSERT INTO Tickets VALUES (?,?,?,?,?)', tickets)
    c.executemany('INSERT INTO TicketMessages VALUES (?,?,?,?,?)', messages)
    c.executemany('INSERT INTO SatisfactionSurveys VALUES (?,?,?,?)', surveys)
    conn.commit(); conn.close()
    
    print("Omni-Production Data Generated. 2000 Orders, 500 Tickets with Surveys.")

if __name__ == "__main__":
    generate_production_data()
