import csv
import random

# Generate Grouped Data: Midpoints and corresponding frequencies
# Group midpoints will range from 100 to 5000, with a step size of 500
group_midpoints = [i for i in range(100, 5050, 500)]
group_frequencies = [random.randint(5, 50) for _ in group_midpoints]  # Random frequencies for each group

# Define the filename
filename = "grouped_sales_data.csv"

# Write the CSV file with only grouped data
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write header for grouped data
    writer.writerow(['Grouped Data (Midpoints)', 'Frequency'])
    
    # Write the grouped data (midpoints and frequencies)
    for midpoint, frequency in zip(group_midpoints, group_frequencies):
        writer.writerow([midpoint, frequency])

print(f"Generated {filename} with grouped data.")
