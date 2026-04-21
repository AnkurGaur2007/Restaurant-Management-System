# 🍽️ Restaurant Management System

A simple **Restaurant Management System** built using **Python (Tkinter GUI)** that helps manage customer orders, billing, reservations, and records efficiently.

---

## 📌 Features

* 🧾 **Order Management**

  * Select items from menu
  * Enter quantity
  * Auto bill calculation

* 💰 **Billing System**

  * Calculates total price
  * Applies **GST (18%)**
  * Displays final bill with breakdown

* 👤 **Customer Details**

  * Stores customer name and contact
  * Validates contact input (numeric only)

* 📊 **Past Records**

  * Saves all orders in a CSV file
  * View previous transactions with details

* 📅 **Reservations System**

  * Make new reservations
  * View all reservations

* 🧹 **Clear Selection**

  * Reset all selected items and inputs instantly

* 📄 **Live Bill Preview**

  * Real-time bill updates as items are added

---

## 🛠️ Technologies Used

* **Python**
* **Tkinter** (GUI)
* **CSV** (data storage)
* **File Handling**

---

## 📂 Project Structure

```
Restaurant-Management-System/
│
├── main.py                # Main application file
├── menu.csv              # Menu items with prices
├── records.csv           # Stored order records
├── reservations.txt      # Reservation data
└── README.md             # Project documentation
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/your-username/restaurant-management-system.git
cd restaurant-management-system
```

2. **Ensure Python is installed**

```bash
python --version
```

3. **Run the application**

```bash
python main.py
```

---

## 📄 Menu File Format (`menu.csv`)

```
Item Name,Price
Burger,120
Pizza,250
Pasta,180
```

---

## 💾 Records File (`records.csv`)

Stores:

* Order Time
* Customer Name
* Contact
* Selected Items
* Total Price
* GST
* Grand Total

---

## 📅 Reservations File (`reservations.txt`)

Stores reservations in plain text format:

```
Name: John, Contact: 1234567890, Date: 2026-04-20, Time: 07:00 PM, Number of People: 4
```

---

## 🚀 Future Improvements

* Database integration (MySQL / SQLite)
* User authentication system
* Enhanced UI design
* Export bills as PDF
* Table management system

---

## ⚠️ Limitations

* Uses local file storage (not scalable)
* Basic UI (Tkinter)
* No concurrency handling

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork this repo and submit a pull request.

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

Developed as a simple desktop-based restaurant management solution using Python.

---

⭐ If you find this project useful, consider giving it a star!
