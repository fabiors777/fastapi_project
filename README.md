# 🍕 FastAPI Orders API

A modern, clean and efficient **Order Management REST API** built with **FastAPI**, featuring secure authentication, user management and complete order workflows.  
This project was designed to be simple to understand, easy to extend, and ready for real-world use cases.

---

## 🚀 Overview

This API provides a full flow for handling users and orders, including:

- User creation and authentication  
- JWT-based login and token refresh  
- Creating and managing orders  
- Adding and removing items inside orders  
- Finishing or canceling orders  
- Listing orders globally (admin) or per user  

All endpoints are documented and available through an auto-generated **Swagger UI**:


---

## ✨ Features

### 🔐 Authentication
- Secure JWT access tokens  
- Login with JSON body or form-data  
- Token refresh endpoint  
- All protected routes require Bearer authentication  

### 👤 User Management
- Create accounts  
- Login and get tokens  
- Access control for protected routes  

### 📦 Orders System
- Create and manage orders  
- Item-level operations inside each order  
- Automatic price updating  
- Order statuses: open, canceled, finished  
- Admin-only and user-only listings  

### 🧩 Schemas & Validation
- Strict Pydantic validation  
- Clean, predictable request/response structures  

### ⚙️ Tech Stack
- FastAPI  
- SQLAlchemy ORM  
- Pydantic  
- SQLite database  
- python-jose (JWT)  
- Passlib (password hashing)  
- python-dotenv  

---

## 📂 Project Structure (Conceptual)

- **Authentication Layer:** login, token generation, secure password hashing, and user registration.  
- **Order Module:** all business logic for managing orders and their items.  
- **Database Models:** structured with SQLAlchemy relationships for users, orders and items.  
- **Schemas:** input/output validation for clean and safe data handling.  
- **Security Layer:** JWT creation, validation and token refresh.  
- **Dependencies:** session management and authentication guards.

---

## 🌐 Main Endpoints

### **Authentication**
- `POST /auth/create_account` — Create a new user  
- `POST /auth/login` — Login using JSON  
- `POST /auth/login-form` — Login using form-data (Swagger compatible)  
- `GET /auth/refresh` — Refresh token  

### **Orders**
- `POST /orders/order` — Create new order  
- `POST /orders/order/add_item/{order_id}` — Add items  
- `POST /orders/order/remove_item/{order_item_id}` — Remove item  
- `POST /orders/order/cancel/{order_id}` — Cancel order  
- `POST /orders/order/finish/{order_id}` — Finish order  
- `GET /orders/order/{order_id}` — Show order  
- `GET /orders/list` — List all orders (admin only)  
- `GET /orders/list/user` — List orders of the logged-in user  


## 💡 Future Enhancements

- Add Docker deployment  
- Add user roles and permissions  
- Add automated tests  
- Support for multiple payment methods  
- Order history and reporting  

---

## 👨‍💻 Author

**Fábio Ribeiro de Souza**

Geographer • Data Engineer • Geospatial Innovation Lead  
Specialist in GIS, geoprocessing, environmental analysis, API development and cloud infrastructure.  
Creator of advanced geospatial and data-driven solutions.

📎 **LinkedIn:** https://www.linkedin.com/in/fabio-ribeiro-de-souza-60007710  
📎 **GitHub:** https://github.com/fabiors777 

---

## ⭐ Contribute

If you found this project useful:

- Star the repository  
- Share feedback  
- Open issues  
- Suggest improvements  

Your support helps the project grow!

---

Thank you for exploring this API! 🚀  
