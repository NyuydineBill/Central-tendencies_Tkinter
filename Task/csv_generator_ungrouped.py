import csv
import random

# Define the range for ungrouped data
min_value = 100
max_value = 5000
num_data_points = 200  # Number of ungrouped data points to generate

# Generate random ungrouped data
ungrouped_data = [random.randint(min_value, max_value) for _ in range(num_data_points)]

# Define the filename
filename = "ungrouped_sales_data.csv"

# Write the CSV file with ungrouped data
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write header for ungrouped data
    writer.writerow(['Ungrouped Data (Values)'])
    
    # Write each data point in a new row
    for value in ungrouped_data:
        writer.writerow([value])

print(f"Generated {filename} with ungrouped data.")
