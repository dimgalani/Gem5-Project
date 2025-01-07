import matplotlib.pyplot as plt
import os
print("Current working directory: ", os.getcwd())
# Function to read and extract data from the text file
def extract_cpi_values(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    benchmarks = []
    cpi_values = []

    # Skip the first two lines (headers) and process the rest
    for line in lines[7:]:
        parts = line.split()
        if len(parts) > 2:  # Ensure the line has enough parts
            benchmarks.append(parts[0])
            cpi_values.append(float(parts[2]))  # Second column (index 2)

    return benchmarks, cpi_values

# Create a directory to save the plots if it doesn't exist
output_dir = "./plots"
os.makedirs(output_dir, exist_ok=True)


# Function to save individual plots
def save_plot(name, benchmarks, cpi_values, file_name):
    plt.figure()
    plt.plot(benchmarks, cpi_values, marker='o', linestyle='-', label=file_name, color='#89CFF0')
    plt.title(f"CPI of {name} across Different Executions", fontsize=10)
    plt.xlabel('Executions', fontsize=8)
    plt.ylabel('CPI Values', fontsize=8)
    plt.xticks(rotation=20, fontsize=6)
    plt.grid(alpha=0.5)
    plt.legend(fontsize=6)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"cpi_{name}.png"))
    plt.close()


# List of input text files
file_paths = [
    "./res-bzip.txt",
    "./res-hmmer.txt",
    "./res-libm.txt",
    "./res-mcf.txt",
    "./res-sjeng.txt"
]

names = ["bzip", "hmmer", "libm", "mcf", "sjeng"]

# Save individual plots for each file
for path, name in zip(file_paths, names):
    benchmarks, cpi_values = extract_cpi_values(path)
    file_name = os.path.basename(path)
    save_plot(name, benchmarks, cpi_values, file_name)
