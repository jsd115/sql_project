"""
This file contains the code to create a Dash application that displays the results of the SQL queries in a dashboard. The application contains six tabs, each displaying a different visualization of the data. The data is read from a CSV file and inserted into an in-memory SQLite database. The SQL queries are executed on the database to extract the required information for the visualizations. The visualizations are created using Plotly and displayed in the Dash application.
"""

# Import required libraries
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html

# Import SQL queries from queries.py
from queries import *

# Read the data from the CSV file
data = pd.read_csv('digital_wallet_transactions.csv')

# Drop the 'idx' column from the data
data = data.drop('idx', axis=1)

# Create a connection to an SQLite database in memory
conn = sqlite3.connect(':memory:')

# Create a cursor object using the connection
# Cursor is used to execute SQL queries
cursor = conn.cursor()

# Create a table in the database
# These columns are the columns in the pandas DataFrame
# The information is gathered from the data_exploration.ipynb file
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

# Insert data into the table from the pandas DataFrame
# Create a for loop to iterate over the rows of the DataFrame
for index, row in data.iterrows():
    # Insert each row into the table
    cursor.execute('''
    INSERT INTO digital_wallet_transaction (
        transaction_id, user_id, transaction_date, product_category, product_name, 
        merchant_name, product_amount, transaction_fee, cashback, loyalty_points, 
        payment_method, transaction_status, merchant_id, device_type, location
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', 
    # Use the values from the row to insert into the table
    (
        row['transaction_id'], row['user_id'], row['transaction_date'], row['product_category'], row['product_name'], 
        row['merchant_name'], row['product_amount'], row['transaction_fee'], row['cashback'], row['loyalty_points'], 
        row['payment_method'], row['transaction_status'], row['merchant_id'], row['device_type'], row['location']
    ))

# Read SQL data into a pandas DataFrame for each query from queries.py
df_query_1 = pd.read_sql_query(query_1, conn)
df_query_2 = pd.read_sql_query(query_2, conn)
df_query_3 = pd.read_sql_query(query_3, conn)
df_query_4 = pd.read_sql_query(query_4, conn)
df_query_5 = pd.read_sql_query(query_5, conn)
df_query_6 = pd.read_sql_query(query_6, conn)

# Commit changes and close the cursor
conn.commit()
conn.close()

# Define colors for the payment method plot
colors = ['orange', 'blue', 'green', 'red', 'purple', 'brown', 'pink', 'yellow', 'grey']

# Define colors for the device usage plot
colors_device_usage = ['orange', 'blue', 'purple']

# Extract unique device types
device_types = df_query_3['device_type'].unique()

# Create a list to hold the bar objects
bars = []

# Iterate over each device type and create a bar for it
for i, device_type in enumerate(device_types):
    filtered_df = df_query_3[df_query_3['device_type'] == device_type]
    bars.append(
        go.Bar(
            x=filtered_df['location'],
            y=filtered_df['count_device_type_by_location'],
            name=device_type,
            marker=dict(color=colors_device_usage[i]),
            text=filtered_df['device_type'],
            hoverinfo='text+y'
        )
    )

# Extract unique payment methods
payment_methods = df_query_5['payment_method'].unique()

# Create a list to hold the bar objects
payment_method_bars = []

# Iterate over each payment method and create a bar for it
for i, payment_method in enumerate(payment_methods):
    payment_method_filtered_df = df_query_5[df_query_5['payment_method'] == payment_method]
    payment_method_bars.append(
        go.Bar(
            x=payment_method_filtered_df['location'],
            y=payment_method_filtered_df['count_payment_method_by_location'],
            name=payment_method,
            marker=dict(color=colors[i % len(colors)]),  # Cycle through colors if there are more payment methods than colors
            text=payment_method_filtered_df['payment_method'],
            hoverinfo='text+y'
        )
    )

# Create a Dash application instance
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    # Heading for the dashboard, displayed on the top of the page
    html.H1('Digital Wallet Transactions Dashboard'),

    # Tabs for different visualizations
    dcc.Tabs([
        # Each tab contains a different visualization
        # First tab displays Locations Sorted by the Average Product Amount
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
                        title='Locations Sorted by the Average Product Amount',
                        barmode='group'
                    )
                )
            )
        ]),
        # The second tab displays the sum of product amount by product category
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
        # The third tab displays the Count of Different Device Usages in the Regions sorted by Average Sales
        dcc.Tab(label='Device Usage', children=[
            dcc.Graph(
                figure=go.Figure(
                    data=bars,
                    layout=go.Layout(
                        title='Count of Different Device Usages in the Regions sorted by Average Sales',
                        barmode='group'
                    )
                )
            )
        ]),
        # The fourth tab displays the Top Ten Most Popular Merchant Names
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
        # The fifth tab displays the Payment Methods in the regions
        dcc.Tab(label='Payment Methods', children=[
            dcc.Graph(
                figure=go.Figure(
                    data=payment_method_bars,
                    layout=go.Layout(
                        title='Payment Methods in Regions',
                        barmode='group'
                    )
                )
            )
        ]),
        # The sixth tab displays the Regions with the Most Loyalty Points
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
                        title='Regions sorted by the Most Loyalty Points',
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