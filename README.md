# 🏭 Factory Inventory Management System

A Django-based web application designed to manage factory operations including inventory, orders, customers, logistics, and financial transactions in a structured and efficient way.

This system provides an integrated solution for handling stock tracking, order processing, dispatch management, and invoicing, making it suitable for small to mid-scale manufacturing units.

---

## 🚀 Features

### 📦 Inventory Management
- Add and manage products
- Track stock levels in real-time
- Maintain stock history and updates

### 🧾 Order Management
- Create and manage customer orders
- Allocate stock to orders
- Lock allocations to prevent conflicts
- Order tracking and status management

### 👥 Customer Management
- Add and manage customer details
- View customer order history
- Maintain customer database

### 🚚 Logistics Management
- Manage dispatch operations
- Generate printable invoices
- Track delivery status

### 💰 Accounting Module
- Create invoices
- Record payments
- Track outstanding balances
- Maintain financial records

### 🔐 Authentication System
- User login system
- Role-based dashboards
- Secure access control

---

## 🏗️ Project Structure

FactoryInventoryManagmentSystem/
│
├── account/          
├── authentication/   
├── customer/         
├── logistics/        
├── order/            
├── stock/            
│
├── templates/        
├── static/           
│
├── manage.py         
└── settings.py       

---

## ⚙️ Tech Stack

- Backend: Django (Python)
- Frontend: HTML, CSS
- Database: SQLite
- Architecture: Django MVT Pattern

---

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/Factory-Inventory-Managment-System.git
cd Factory-Inventory-Managment-System
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install django
```

### 4. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser
```bash
python manage.py createsuperuser
```

### 6. Run the server
```bash
python manage.py runserver
```

### 7. Open in browser
```
http://127.0.0.1:8000/
```

---

## 📊 Modules Overview

| Module        | Description                          |
|--------------|--------------------------------------|
| Stock        | Product and inventory tracking       |
| Order        | Order creation and stock allocation  |
| Customer     | Customer records management          |
| Logistics    | Dispatch and delivery tracking       |
| Account      | Invoices and payments                |
| Auth         | Login and role management            |

---

## 🔒 Key Functional Concepts

- Stock Allocation Logic → Prevents over-allocation
- Order Locking Mechanism → Ensures consistency
- Role-Based Dashboards → Different UI for users

---

## 🎯 Future Improvements

- Advanced analytics dashboard
- Real-time notifications
- Cloud deployment (AWS / Render)

---

## 🧠 Learning Outcomes

- Real-world Django application architecture
- Handling multiple interconnected modules
- Database design and relationships
- Backend-driven UI rendering
- Business logic implementation

---

## 📌 Use Case

- Specifically for Ceramic industry
- Small manufacturing units
- Warehouses

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 👨‍💻 Author

Naman Ashani  
Ronit Vyas  
Prutha Aghara  

---

## ER Diagram
![ER diagram ](https://github.com/user-attachments/assets/295a0eb2-afcb-4380-ac4b-680b14391664)

