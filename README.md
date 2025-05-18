# 🏫 Room Allocation System

A web-based Room Allocation System built with **Python (Flask)** for dynamically assigning students to rooms while ensuring that students from the same year are not seated together. Includes a user-friendly interface and database integration.

---

## 🚀 Features

- 📊 **Dynamic room allocation** based on student year and room capacity
- ❌ **No same-year students** are seated next to each other
- 🧮 **500+ student records** and **15+ room entries**
- 🔍 **Search by Student ID** to view individual allocation
- 🏠 **View room-wise student list**
- ✅ **Confirmation popup** after allocation
- 📁 **SQLite database integration** for persistent data storage
- ⚡ Built using **Flask**, **HTML/CSS**, **JavaScript**, and **Bootstrap**

---

## 🖥️ Tech Stack

- Backend: **Python (Flask)**
- Frontend: **HTML, CSS, JavaScript**
- Database: **SQLite**
- Tools: **Git, GitHub**

---

## 📂 Project Structure

Room_allocation_system/
├── app.py # Main Flask application
├── allocator.py # Logic for allocating students to rooms
├── database.py # DB initialization and data seeding
├── /templates/
│ └── index.html # Frontend HTML
├── /static/
│ ├── style.css # Custom CSS
│ └── script.js # JavaScript for UI interaction
├── /instance/
│ └── allocation.db # SQLite database
└── README.md # Project documentation

---

## 🛠️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/ctrl-piyush/Room_allocation_system.git
   cd Room_allocation_system
2.Create and activate a virtual environment
  python -m venv venv
  venv\Scripts\activate   # On Windows
3.Install dependencies
  pip install -r requirements.txt
4.Initialize the database
  python database.py
5.Run the application
  python app.py
6.Open in browser
  Visit http://127.0.0.1:5000
