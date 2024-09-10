"""
This file contains the queries that will be used to extract data from the database.
"""

# Query to find the top 10 locations with the highest average product_amount
query_1 = """
SELECT location, avg(product_amount) as avg_product_amount_by_location 
FROM digital_wallet_transaction
GROUP BY location
ORDER BY avg_product_amount_by_location DESC
LIMIT 10
"""

# Query to find the sum of product_amount by product_category
query_2 = """
SELECT product_category, sum(product_amount) as sum_product_amount_by_category
FROM digital_wallet_transaction
GROUP BY product_category
"""

# Query to find the count of different device usages in the 10 regions with the avg sales
query_3 = """
SELECT location, device_type, count(device_type) as count_device_type_by_location 
FROM digital_wallet_transaction
GROUP BY location, device_type
ORDER BY count_device_type_by_location DESC
LIMIT 10
"""

# Query to find the top ten most popular merchant names
query_4 = """
SELECT merchant_name, COUNT(merchant_name) as count_merchant_name 
FROM digital_wallet_transaction
GROUP BY merchant_name
ORDER BY count_merchant_name DESC
LIMIT 10
"""

# Query to find the most popular payment methods in the 10 regions where avg product amount is the lowest 
query_5 = """
SELECT location, payment_method, count(payment_method) as count_payment_method_by_location, avg(product_amount) as avg_product_amount_by_location
FROM digital_wallet_transaction
GROUP BY location, payment_method
ORDER BY avg_product_amount_by_location ASC
LIMIT 10
"""

# Find the regions with the most loyalty_points
query_6 = """
SELECT location, sum(loyalty_points) as sum_loyalty_points_by_location
FROM digital_wallet_transaction
GROUP BY location
ORDER BY sum_loyalty_points_by_location DESC
LIMIT 10
"""