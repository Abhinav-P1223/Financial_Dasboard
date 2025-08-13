# 💰 Bank Transaction Dashboard

A web-based banking dashboard built using **Flask**, **MySQL**, and **Matplotlib** that provides insights into user transactions with interactive filters and visualizations like moving average graphs and pie charts.

---

## 🚀 Features

- User transaction data stored in a MySQL database
- View and filter transactions by **account holder name**
- Select **date range** for visual analysis
- **Moving Average** graph with customizable window size (e.g., 3 days, 7 days)
- **Pie chart** showing transaction type distribution (debit in red, credit in green) with labels
- Clean and responsive UI using **Bootstrap**

---

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.x
- MySQL Server
- pip (Python package manager)

### MySQL Database Setup

1. Open MySQL and run:
    ```sql
    CREATE DATABASE bank;
    USE bank;
    ```

2. Create tables:
    ```sql
    CREATE TABLE transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        date DATE,
        type ENUM('debit', 'credit'),
        amount DECIMAL(10,2)
    );
    ```

3. Insert sample data (optional):
    ```sql
    INSERT INTO transactions (name, date, type, amount) VALUES
    ('John Doe', '2025-08-01', 'debit', 100.00),
    ('John Doe', '2025-08-02', 'credit', 200.00),
    ('Jane Smith', '2025-08-02', 'debit', 300.00);
    ```

---

## ⚙️ Python Setup

1. Clone the repository or place your project files in a folder:
    ```
    git clone <your-repo-url>
    cd bank-dashboard
    ```

2. Install required libraries:
    ```
    pip install flask mysql-connector-python matplotlib
    ```

3. Update database credentials in `app.py`:
    ```python
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'bank'
    }
    ```

4. Run the app:
    ```
    python app.py
    ```

5. Open in your browser:
    ```
    http://localhost:5000
    ```

---

## 📊 Usage

- Select a user from the dropdown
- Choose a **date range**
- Set the **moving average window (in days)** (e.g., 3, 5, 7)
- Click **"Apply Filters"**
- Dashboard displays:
  - **Moving average line graph** of transaction amounts
  - **Pie chart** showing debit vs credit share

---

## 📁 Project Structure

├── app.py
├── templates/
│ └── dashboard.html
├── static/
│ └── charts/
│ ├── moving_avg.png
│ └── pie_chart.png
└── README.md


---

## 🧠 Customization Ideas

- Add user authentication
- Add download option for filtered data (CSV/Excel)
- More charts: Monthly spending trends, category-wise expenses
- Use Chart.js for interactive graphs

## Results



## 📃 License

This project is for educational purposes. Modify and use freely.
