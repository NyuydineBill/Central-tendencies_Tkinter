

# Central Tendency Calculator

This is a **Central Tendency Calculator** built using **Python** and **Tkinter**, with support for importing CSV data and performing statistical analysis for both ungrouped and grouped data. The calculator computes measures of central tendency and dispersion such as **mean, median, mode, variance, standard deviation, range, quartiles**, and more.

## Features
- Supports both **ungrouped** and **grouped** data.
- Allows manual input or **CSV file import** for data.
- Calculates key statistics including:
  - Mean
  - Median
  - Mode
  - Variance
  - Standard deviation
  - Range
  - 1st and 3rd Quartiles (Q1 and Q3)
  - Interquartile Range (IQR)
- Plots histograms for ungrouped data and bar charts for grouped data.

## Data Input
- **Ungrouped data**: Enter numbers separated by commas, or import a CSV file with a single column of numbers.
- **Grouped data**: Enter group midpoints and frequencies separated by commas, or import a CSV file with two columns (one for midpoints and one for frequencies).

### Example Data
- **Ungrouped**: `1.5, 2.5, 3.5, 4.5, 5.5`
- **Grouped**: Midpoints: `10, 20, 30`, Frequencies: `5, 10, 8`

## Installation
1. Clone the repository or download the program.
2. Install the required dependencies by running:
   ```bash
   pip install numpy scipy matplotlib pandas tk
   ```
3. Run the program:
   ```bash
   python central_tendency_calculator.py
   ```

## Usage
1. Start the program and choose whether your data is **ungrouped** or **grouped** using the dropdown.
2. Enter your data manually or click the **Import CSV** button to load data from a file.
3. Click **Calculate** to compute the statistics.
4. For ungrouped data, a histogram with additional statistics is displayed. For grouped data, a bar chart is shown.

### CSV Import Format
- For **ungrouped data**: A single column of numbers.
- For **grouped data**: Two columns, the first for midpoints and the second for frequencies.

## Error Handling
- The program will alert you if there are input errors, such as:
  - Missing data
  - Incorrect CSV format
  - Mismatch in group and frequency lengths

## Dependencies
- `Tkinter`: For the graphical user interface
- `Numpy`: For numerical computations
- `Scipy`: For statistical operations
- `Matplotlib`: For plotting histograms and charts
- `Pandas`: For handling CSV file imports

## Author
Nyuydine Bill

