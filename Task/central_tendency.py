import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Welcome screen
def welcome_screen():
    messagebox.showinfo(
        "Welcome to Central Tendency Calculator",
        "This tool will help you calculate measures of central tendency and dispersion.\n\n"
        "For Ungrouped data:\n1. Enter numbers separated by commas.\n\n"
        "For Grouped data:\n1. Enter group midpoints and frequencies separated by commas.\n"
        "2. Measures include mean, median, mode, variance, standard deviation, range, and more."
    )

# Show/hide fields based on data type
def toggle_fields(*args):
    if data_type.get() == "Ungrouped":
        label.pack()
        entry_data.pack()
        label_groups.pack_forget()
        entry_data_groups.pack_forget()
        label_frequencies.pack_forget()
        entry_groups.pack_forget()
    else:
        label.pack_forget()
        entry_data.pack_forget()
        label_groups.pack()
        entry_data_groups.pack()
        label_frequencies.pack()
        entry_groups.pack()

# Calculate central tendency and dispersion
def calculate_statistics():
    try:
        if data_type.get() == "Ungrouped":
            # Get ungrouped data input
            data_input = entry_data.get()
            data = list(map(float, data_input.split(',')))

            # Central tendency measures
            mean = np.mean(data)
            median = np.median(data)
            mode_result = stats.mode(data, keepdims=True)
            mode_value = mode_result.mode[0] if mode_result.count[0] > 0 else "No mode"

            # Dispersion measures
            variance = np.var(data)
            std_deviation = np.std(data)
            data_range = np.ptp(data)  # Range
            q1 = np.percentile(data, 25)  # 1st Quartile
            q3 = np.percentile(data, 75)  # 3rd Quartile
            iqr = q3 - q1  # Interquartile Range

            # Display results
            result = (
                f'Mean: {mean:.2f}\n'
                f'Median: {median:.2f}\n'
                f'Mode: {mode_value}\n\n'
                f'Variance: {variance:.2f}\n'
                f'Standard Deviation: {std_deviation:.2f}\n'
                f'Range: {data_range:.2f}\n'
                f'1st Quartile (Q1): {q1:.2f}\n'
                f'3rd Quartile (Q3): {q3:.2f}\n'
                f'Interquartile Range (IQR): {iqr:.2f}'
            )
            messagebox.showinfo("Results", result)
            plot_histogram(data)

        else:  # Grouped data
            # Get frequency input
            freq_input = entry_groups.get()
            data_input = entry_data_groups.get()
            
            groups = list(map(float, data_input.split(',')))
            frequencies = list(map(int, freq_input.split(',')))

            if len(groups) != len(frequencies):
                messagebox.showerror("Input Error", "Groups and Frequencies must have the same length.")
                return

            # Calculate mean for grouped data
            total_frequency = sum(frequencies)
            class_width = groups[1] - groups[0]  # Assumes equal class width
            midpoints = [(groups[i] + (groups[i+1] if i+1 < len(groups) else groups[i])) / 2 for i in range(len(groups))]
            mean_grouped = sum(freq * mid for freq, mid in zip(frequencies, midpoints)) / total_frequency

            cumulative_freq = np.cumsum(frequencies)
            median_index = total_frequency / 2

            # Find median group
            median_group_index = np.argmax(cumulative_freq >= median_index)
            median_group = groups[median_group_index]

            # Mode calculation for grouped data
            modal_class_index = np.argmax(frequencies)
            f1 = frequencies[modal_class_index]
            f0 = frequencies[modal_class_index-1] if modal_class_index > 0 else 0
            f2 = frequencies[modal_class_index+1] if modal_class_index+1 < len(frequencies) else 0
            L = groups[modal_class_index]
            mode_grouped = L + ((f1 - f0) / (2 * f1 - f0 - f2)) * class_width if (2 * f1 - f0 - f2) != 0 else "Undefined"

            # Variance and standard deviation for grouped data
            variance_grouped = sum(freq * (mid - mean_grouped)**2 for freq, mid in zip(frequencies, midpoints)) / total_frequency
            std_deviation_grouped = np.sqrt(variance_grouped)

            # Range
            data_range = groups[-1] - groups[0]

            result = (
                f'Mean: {mean_grouped:.2f}\n'
                f'Median Group: {median_group:.2f}\n'
                f'Mode: {mode_grouped}\n\n'
                f'Variance: {variance_grouped:.2f}\n'
                f'Standard Deviation: {std_deviation_grouped:.2f}\n'
                f'Range: {data_range:.2f}'
            )
            messagebox.showinfo("Results", result)
            plot_grouped_histogram(groups, frequencies)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

# Plot histogram for ungrouped data
def plot_histogram(data):
    mean = np.mean(data)
    median = np.median(data)
    mode_result = stats.mode(data, keepdims=True)
    mode = mode_result.mode[0] if mode_result.count[0] > 0 else None
    variance = np.var(data)
    std_deviation = np.std(data)
    data_range = (np.min(data), np.max(data))
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)

    plt.figure(figsize=(10, 5))
    plt.hist(data, bins=10, alpha=0.7, color='blue', edgecolor='black', label='Data')
    plt.axvline(mean, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {mean:.2f}')
    plt.axvline(median, color='yellow', linestyle='dashed', linewidth=1, label=f'Median: {median:.2f}')
    if mode is not None:
        plt.axvline(mode, color='green', linestyle='dashed', linewidth=1, label=f'Mode: {mode:.2f}')

    # Add standard deviation shading
    plt.fill_betweenx([0, plt.gca().get_ylim()[1]], mean - std_deviation, mean + std_deviation, color='red', alpha=0.1, label=f'±1 Std Dev')
    plt.fill_betweenx([0, plt.gca().get_ylim()[1]], mean - 2 * std_deviation, mean + 2 * std_deviation, color='orange', alpha=0.1, label=f'±2 Std Dev')

    # Add quartiles
    plt.axvline(q1, color='purple', linestyle='dashed', linewidth=1, label=f'Q1: {q1:.2f}')
    plt.axvline(q3, color='purple', linestyle='dashed', linewidth=1, label=f'Q3: {q3:.2f}')

    # Add range lines
    plt.hlines(y=plt.gca().get_ylim()[1] * 0.9, xmin=data_range[0], xmax=data_range[1], color='black', linestyle='dashed', label=f'Range: {data_range[1] - data_range[0]:.2f}')

    plt.title('Histogram of Ungrouped Data')
    plt.xlabel('Data Values')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

# Plot grouped data bar chart
def plot_grouped_histogram(groups, frequencies):
    total_frequency = sum(frequencies)
    class_width = groups[1] - groups[0]
    midpoints = [(groups[i] + (groups[i+1] if i+1 < len(groups) else groups[i])) / 2 for i in range(len(groups))]
    mean_grouped = sum(freq * mid for freq, mid in zip(frequencies, midpoints)) / total_frequency
    cumulative_freq = np.cumsum(frequencies)
    median_index = total_frequency / 2
    median_group_index = np.argmax(cumulative_freq >= median_index)
    median_group = groups[median_group_index]

    modal_class_index = np.argmax(frequencies)
    f1 = frequencies[modal_class_index]
    f0 = frequencies[modal_class_index-1] if modal_class_index > 0 else 0
    f2 = frequencies[modal_class_index+1] if modal_class_index+1 < len(frequencies) else 0
    L = groups[modal_class_index]
    mode_grouped = L + ((f1 - f0) / (2 * f1 - f0 - f2)) * class_width if (2 * f1 - f0 - f2) != 0 else None

    # Calculate approximate quartiles using cumulative frequencies
    q1_index = 0.25 * total_frequency
    q3_index = 0.75 * total_frequency
    q1_group_index = np.argmax(cumulative_freq >= q1_index)
    q3_group_index = np.argmax(cumulative_freq >= q3_index)
    q1_group = groups[q1_group_index]
    q3_group = groups[q3_group_index]

    plt.figure(figsize=(10, 5))
    plt.bar(groups, frequencies, width=class_width, alpha=0.7, color='blue', edgecolor='black', label='Frequency')
    plt.axvline(mean_grouped, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {mean_grouped:.2f}')
    plt.axvline(median_group, color='yellow', linestyle='dashed', linewidth=1, label=f'Median Group: {median_group:.2f}')
    if mode_grouped is not None:
        plt.axvline(mode_grouped, color='green', linestyle='dashed', linewidth=1, label=f'Mode: {mode_grouped:.2f}')

    # Add range line
    plt.hlines(y=max(frequencies) + 0.5, xmin=groups[0], xmax=groups[-1], color='black', linestyle='dashed', label=f'Range: {groups[-1] - groups[0]:.2f}')

    # Add quartiles
    plt.axvline(q1_group, color='purple', linestyle='dashed', linewidth=1, label=f'Q1: {q1_group:.2f}')
    plt.axvline(q3_group, color='purple', linestyle='dashed', linewidth=1, label=f'Q3: {q3_group:.2f}')

    plt.title('Bar Chart of Grouped Data')
    plt.xlabel('Group Midpoints')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

# Create the main window
root = tk.Tk()
root.title("Advanced Central Tendency & Dispersion Calculator")

data_type = tk.StringVar(value="Ungrouped")
data_type.trace('w', toggle_fields)  # Trace changes to toggle fields

# Select Data Type
data_type_frame = tk.Frame(root)
data_type_frame.pack()
tk.Label(data_type_frame, text="Select Data Type:").pack(side=tk.LEFT)
ttk.Radiobutton(data_type_frame, text="Ungrouped", variable=data_type, value="Ungrouped").pack(side=tk.LEFT)
ttk.Radiobutton(data_type_frame, text="Grouped", variable=data_type, value="Grouped").pack(side=tk.LEFT)

# Input for Ungrouped Data
label = tk.Label(root, text="Enter ungrouped numbers (comma-separated):")
entry_data = tk.Entry(root, width=50)

# Input for Grouped Data
label_groups = tk.Label(root, text="Enter group midpoints (comma-separated):")
entry_data_groups = tk.Entry(root, width=50)
label_frequencies = tk.Label(root, text="Enter frequencies (comma-separated):")
entry_groups = tk.Entry(root, width=50)

# Calculate button
calc_button = tk.Button(root, text="Calculate", command=calculate_statistics)
calc_button.pack()

# Run the welcome screen
welcome_screen()

# Run the application
root.mainloop()
