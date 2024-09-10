import sqlite3
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from queries import *

data = pd.read_csv('sql_project/digital_wallet_transactions.csv')
data = data.drop('idx', axis=1)

# Create a connection to an SQLite database (in-memory or a file)
conn = sqlite3.connect(':memory:')  # Use ':memory:' to create a database in RAM
cursor = conn.cursor()

# Create a sample table
cursor.execute('''
CREATE TABLE digital_wallet_transaction (
    transaction_id TEXT PRIMARY KEY,
    user_id TEXT,
    transaction_date TEXT,
    product_category TEXT,
    product_name TEXT,
    merchant_name TEXT,
    product_amount REAL,
    transaction_fee REAL,
    cashback REAL,
    loyalty_points INTEGER,                   
    payment_method TEXT,
    transaction_status TEXT,
    merchant_id TEXT,
    device_type TEXT,
    location TEXT                                                 
)
''')

# Insert sample data
for index, row in data.iterrows():
    cursor.execute('''
    INSERT INTO digital_wallet_transaction (
        transaction_id, user_id, transaction_date, product_category, product_name, 
        merchant_name, product_amount, transaction_fee, cashback, loyalty_points, 
        payment_method, transaction_status, merchant_id, device_type, location
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        row['transaction_id'], row['user_id'], row['transaction_date'], row['product_category'], row['product_name'], 
        row['merchant_name'], row['product_amount'], row['transaction_fee'], row['cashback'], row['loyalty_points'], 
        row['payment_method'], row['transaction_status'], row['merchant_id'], row['device_type'], row['location']
    ))

# Read SQL data into a pandas DataFrame
df_query_1 = pd.read_sql_query(query_1, conn)
df_query_2 = pd.read_sql_query(query_2, conn)
df_query_3 = pd.read_sql_query(query_3, conn)
df_query_4 = pd.read_sql_query(query_4, conn)
df_query_5 = pd.read_sql_query(query_5, conn)
df_query_6 = pd.read_sql_query(query_6, conn)

colors = ['orange', 'blue', 'green', 'red', 'purple', 'brown', 'pink', 'yellow', 'grey']

# Commit changes and close the cursor
conn.commit()
conn.close()

# Create a Dash application
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1('Digital Wallet Transactions Dashboard'),

    dcc.Tabs([
        dcc.Tab(label='Top Locations', children=[
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=df_query_1['location'],
                            y=df_query_1['avg_product_amount_by_location'],
                            name='Average Product Amount',
                            marker=dict(color='blue')
                        )
                    ],
                    layout=go.Layout(
                        title='Top 10 Locations with the Highest Average Product Amount',
                        barmode='group'
                    )
                )
            )
        ]),
        dcc.Tab(label='Product Categories', children=[
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=df_query_2['product_category'],
                            y=df_query_2['sum_product_amount_by_category'],
                            name='Sum of Product Amount',
                            marker=dict(color='green')
                        )
                    ],
                    layout=go.Layout(
                        title='Sum of Product Amount by Product Category',
                        barmode='group'
                    )
                )
            )
        ]),
        dcc.Tab(label='Device Usage', children=[
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=df_query_3['location'],
                            y=df_query_3['count_device_type_by_location'],
                            name='Count of Device Type',
                            marker=dict(color='red')
                        )
                    ],
                    layout=go.Layout(
                        title='Count of Different Device Usages in the 10 Regions with the Average Sales',
                        barmode='group'
                    )
                )
            )
        ]),
        dcc.Tab(label='Merchant Popularity', children=[
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=df_query_4['merchant_name'],
                            y=df_query_4['count_merchant_name'],
                            name='Count of Merchant Name',
                            marker=dict(color='purple')
                        )
                    ],
                    layout=go.Layout(
                        title='Top Ten Most Popular Merchant Names',
                        barmode='group'
                    )
                )
            )
        ]),
        dcc.Tab(label='Payment Methods', children=[
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=df_query_5['location'],
                            y=df_query_5['count_payment_method_by_location'],
                            name='Count of Payment Method',
                            marker=dict(color=colors),
                            text = df_query_5['payment_method'],
                            hoverinfo = 'text+y'
                        )
                    ],
                    layout=go.Layout(
                        title='Payment Methods in least popular regions',
                        barmode='group'
                    )
                )
            )
        ]),
        dcc.Tab(label='Loyalty Points', children=[
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        go.Bar(
                            x=df_query_6['location'],
                            y=df_query_6['sum_loyalty_points_by_location'],
                            name='Sum of Loyalty Points',
                            marker=dict(color='brown')
                        )
                    ],
                    layout=go.Layout(
                        title='Regions with the Most Loyalty Points',
                        barmode='group'
                    )
                )
            )
        ])
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)