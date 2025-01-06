import math

# Define the cost calculation function
def calculate_cost(L1_dsize, L1_dassoc, L1_isize, L1_iassoc, L2_size, L2_assoc, line_size):
    cost = (L1_isize / 32) +(L1_dsize / 32) + (L2_size / 1) + math.exp(0.13 * L1_dassoc)+ math.exp(0.13 * L1_iassoc) + math.exp(0.11 * L2_assoc) + 0.1 * (line_size / 64)
    return cost

# Parse the table from the text file
def process_file(file_path):
    results = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        headers = None

        for line in lines:
            # Skip empty or separator lines
            if line.strip() == "" or line.startswith("| -"):
                continue

            # Parse the row data
            data = [d.strip() for d in line.split('|') if d.strip()]

            try:
                config_name = data[0]
                L1_isize = int(data[3])
                L1_iassoc = int(data[4])
                L1_dsize = int(data[1])
                L1_dassoc = int(data[2])
                L2_size = int(data[5])
                L2_assoc = int(data[6])
                line_size = int(data[7])

                # Calculate cost
                cost = calculate_cost(L1_dsize, L1_dassoc, L1_isize, L1_iassoc, L2_size, L2_assoc, line_size)

                # Add result to list
                results.append(cost)

            except ValueError as e:
                print(f"Error processing line: {line.strip()}, {e}")

    return results

# Write results to a file
def write_results(results, output_path):
    with open(output_path, 'w') as file:
        file.write("Cost\n")
        for cost in results:
            file.write(f"{cost:.4f}\n")


input_file = "./exp_table_specs.txt"
output_file = "cache_costs.txt"
results = process_file(input_file)
write_results(results, output_file)