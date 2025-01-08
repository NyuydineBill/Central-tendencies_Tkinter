import tkinter as tk
from tkinter import messagebox, ttk, filedialog  # Added filedialog
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd  

# Welcome screen
def welcome_screen():
    messagebox.showinfo(
        "Welcome to Central Tendency Calculator",
        "Hello COME400!\n"
        "This tool will help you calculate measures of central tendency and dispersion.\n\n"
        "For Ungrouped data:\n1. Enter numbers separated by commas.\n"
        "   OR\n2. Import a CSV file with a single column of numbers.\n\n"
        "For Grouped data:\n1. Enter group midpoints and frequencies separated by commas.\n"
        "   OR\n2. Import a CSV file with two columns: 'Midpoints' and 'Frequencies'.\n\n"
        "Measures include mean, median, mode, variance, standard deviation, range, quartiles, and more."
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
    
    # Always show the Import CSV button
    btn_import.pack()


# Function to import CSV
def import_csv():
    try:
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        if not file_path:
            return  # User cancelled the file dialog

        df = pd.read_csv(file_path)

        if data_type.get() == "Ungrouped":
            if df.shape[1] != 1:
                messagebox.showerror("Format Error", "Ungrouped data CSV must have exactly one column.")
                return
            # Convert the single column to a comma-separated string
            data = df.iloc[:, 0].dropna().astype(float).tolist()
            entry_data.delete(0, tk.END)
            entry_data.insert(0, ','.join(map(str, data)))
        else:  # Grouped data
            if df.shape[1] < 2:
                messagebox.showerror("Format Error", "Grouped data CSV must have at least two columns: 'Midpoints' and 'Frequencies'.")
                return
            # Assume first two columns are Midpoints and Frequencies
            midpoints = df.iloc[:, 0].dropna().astype(float).tolist()
            frequencies = df.iloc[:, 1].dropna().astype(int).tolist()
            entry_data_groups.delete(0, tk.END)
            entry_groups.delete(0, tk.END)
            entry_data_groups.insert(0, ','.join(map(str, midpoints)))
            entry_groups.insert(0, ','.join(map(str, frequencies)))
        
        messagebox.showinfo("Success", "CSV data imported successfully!")
    except Exception as e:
        messagebox.showerror("Import Error", f"An error occurred while importing CSV:\n{e}")

# Calculate central tendency and dispersion
def calculate_statistics():
    try:
        if data_type.get() == "Ungrouped":
            # Get ungrouped data input
            data_input = entry_data.get()
            if not data_input.strip():
                messagebox.showerror("Input Error", "Please enter ungrouped data or import a CSV file.")
                return
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
            
            if not data_input.strip() or not freq_input.strip():
                messagebox.showerror("Input Error", "Please enter grouped data or import a CSV file.")
                return

            groups = list(map(float, data_input.split(',')))
            frequencies = list(map(int, freq_input.split(',')))

            if len(groups) != len(frequencies):
                messagebox.showerror("Input Error", "Groups and Frequencies must have the same length.")
                return

            # Calculate mean for grouped data
            total_frequency = sum(frequencies)
            if total_frequency == 0:
                messagebox.showerror("Computation Error", "Total frequency cannot be zero.")
                return

            class_width = groups[1] - groups[0] if len(groups) > 1 else 1  # Handle single group case
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

            # Calculate quartiles
            q1 = 0.25 * total_frequency
            q3 = 0.75 * total_frequency
            q1_group_index = np.argmax(cumulative_freq >= q1)
            q3_group_index = np.argmax(cumulative_freq >= q3)
            q1_group = groups[q1_group_index]
            q3_group = groups[q3_group_index]

            result = (
                f'Mean: {mean_grouped:.2f}\n'
                f'Median Group: {median_group:.2f}\n'
                f'Mode: {mode_grouped}\n\n'
                f'Variance: {variance_grouped:.2f}\n'
                f'Standard Deviation: {std_deviation_grouped:.2f}\n'
                f'Range: {data_range:.2f}\n'
                f'1st Quartile (Q1): {q1_group:.2f}\n'
                f'3rd Quartile (Q3): {q3_group:.2f}'
            )
            messagebox.showinfo("Results", result)
            plot_grouped_histogram(groups, frequencies)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

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
    if total_frequency == 0:
        messagebox.showerror("Plot Error", "Total frequency is zero. Cannot plot histogram.")
        return

    class_width = groups[1] - groups[0] if len(groups) > 1 else 1  # Handle single group case
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

    # Calculate quartiles
    q1 = 0.25 * total_frequency
    q3 = 0.75 * total_frequency
    q1_group_index = np.argmax(cumulative_freq >= q1)
    q3_group_index = np.argmax(cumulative_freq >= q3)
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
data_type_frame.pack(pady=10)
tk.Label(data_type_frame, text="Select Data Type:").pack(side=tk.LEFT, padx=5)
ttk.Radiobutton(data_type_frame, text="Ungrouped", variable=data_type, value="Ungrouped").pack(side=tk.LEFT, padx=5)
ttk.Radiobutton(data_type_frame, text="Grouped", variable=data_type, value="Grouped").pack(side=tk.LEFT, padx=5)

# Input for Ungrouped Data
label = tk.Label(root, text="Enter ungrouped numbers (comma-separated):")
entry_data = tk.Entry(root, width=60)

# Input for Grouped Data
label_groups = tk.Label(root, text="Enter group midpoints (comma-separated):")
entry_data_groups = tk.Entry(root, width=60)
label_frequencies = tk.Label(root, text="Enter frequencies (comma-separated):")
entry_groups = tk.Entry(root, width=60)

# Import CSV Button
btn_import = tk.Button(root, text="Import CSV", command=import_csv)

# Calculate button
calc_button = tk.Button(root, text="Calculate", command=calculate_statistics)
calc_button.pack(pady=10)

# Initially pack the appropriate fields
toggle_fields()

# Run the welcome screen
welcome_screen()

# Run the application
root.mainloop()