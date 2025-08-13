from flask import Flask, render_template, request
import mysql.connector
import matplotlib
matplotlib.use('Agg')  # Non-GUI backend
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/charts'

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yourpassword',  # Replace with your MySQL password
    'database': 'bank'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def generate_charts(transactions, window):
    if not transactions:
        return None, None, None

    df = pd.DataFrame(transactions)
    df['txn_date'] = pd.to_datetime(df['txn_date'])
    df = df.sort_values('txn_date')

    # Compute moving average
    df['moving_avg'] = df['balance'].rolling(window=window, min_periods=1).mean()

    # Count transaction types
    types = {'Debit': 0, 'Credit': 0}
    for t in transactions:
        if t['DrCr'] == 'Db':
            types['Debit'] += 1
        elif t['DrCr'] == 'Cr':
            types['Credit'] += 1

    # Clear previous charts
    for f in os.listdir(app.config['UPLOAD_FOLDER']):
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
        except Exception:
            pass

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # 1. Line Chart - Balance Over Time
    plt.figure(figsize=(10, 4))
    plt.plot(df['txn_date'], df['balance'], marker='o', color='blue', label='Daily Balance')
    plt.title("Balance Over Time")
    plt.xlabel("Date")
    plt.ylabel("Balance (₹)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    line_filename = f'line_chart_{timestamp}.png'
    plt.savefig(os.path.join(app.config['UPLOAD_FOLDER'], line_filename))
    plt.close()

    # 2. Moving Average Chart
    plt.figure(figsize=(10, 4))
    plt.plot(df['txn_date'], df['balance'], label='Daily Balance', alpha=0.4, linestyle='--')
    plt.plot(df['txn_date'], df['moving_avg'], label=f'{window}-Day Moving Avg', color='orange', linewidth=2)
    plt.title(f"{window}-Day Moving Average of Balance")
    plt.xlabel("Date")
    plt.ylabel("Balance (₹)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    moving_avg_filename = f'moving_avg_{timestamp}.png'
    plt.savefig(os.path.join(app.config['UPLOAD_FOLDER'], moving_avg_filename))
    plt.close()

    # 3. Pie Chart - Transaction Type Distribution
    plt.figure(figsize=(6, 6))
    labels = list(types.keys())
    sizes = list(types.values())
    colors = ['red', 'green']
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        colors=colors,
        startangle=140,
        textprops={'color': "white"}
    )
    plt.legend(wedges, labels, title="Transaction Type", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.title("Transaction Type Distribution (Debit vs Credit)")
    plt.tight_layout()
    pie_filename = f'pie_chart_{timestamp}.png'
    plt.savefig(os.path.join(app.config['UPLOAD_FOLDER'], pie_filename))
    plt.close()

    return line_filename, moving_avg_filename, pie_filename

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    name = request.form.get('username', '').strip()
    tr_type = request.form.get('tr_type', '')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    window = request.form.get('window', '7')

    try:
        window = max(1, int(window))
    except ValueError:
        window = 7

    query = "SELECT txn_date, DrCr, amount, balance, user_name FROM statements WHERE 1=1"
    params = []

    if name:
        query += " AND LOWER(user_name) = LOWER(%s)"
        params.append(name)

    if tr_type in ['Db', 'Cr']:
        query += " AND DrCr = %s"
        params.append(tr_type)

    if start_date:
        query += " AND txn_date >= %s"
        params.append(start_date)

    if end_date:
        query += " AND txn_date <= %s"
        params.append(end_date)

    query += " ORDER BY txn_date ASC"

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, tuple(params))
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()

    line_chart, moving_avg_chart, pie_chart = generate_charts(transactions, window)

    return render_template(
        'dashboard.html',
        transactions=transactions,
        filter_name=name,
        tr_type=tr_type,
        start_date=start_date,
        end_date=end_date,
        line_chart=line_chart,
        moving_avg_chart=moving_avg_chart,
        pie_chart=pie_chart,
        window=window
    )

@app.route('/charts')
def charts():
    return render_template(
        'charts.html',
        line_chart=request.args.get('line_chart'),
        moving_avg_chart=request.args.get('moving_avg_chart'),
        pie_chart=request.args.get('pie_chart')
    )

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
