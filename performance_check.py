import psutil, time, csv, random
import GA, SA, ACO

import matplotlib.pyplot as plt
import pandas as pd

def monitor_resources(func, *args, **kwargs):
    """Monitors CPU and RAM usage while running a function."""
    process = psutil.Process()
    start_time = time.time()
    
    # Measure initial memory usage
    initial_memory = process.memory_info().rss 
    
    # Start measuring CPU usage
    initial_cpu_times = process.cpu_times()
    
    # Execute the algorithm
    result = func(*args, **kwargs)
    
    # Measure final CPU usage
    final_cpu_times = process.cpu_times()
    cpu_time_used = sum([final_cpu_times.user - initial_cpu_times.user,
                         final_cpu_times.system - initial_cpu_times.system])
    
    # Measure final memory usage
    final_memory = process.memory_info().rss
    memory_usage = final_memory - initial_memory
    
    # Total execution time
    elapsed_time = time.time() - start_time

    print("")
    # Print results
    print(f"CPU Time Used: {cpu_time_used:.2f} seconds")
    print(f"Memory Usage: {memory_usage:.2f} B")
    print(f"Execution Time: {elapsed_time:.2f} seconds")
    
    return cpu_time_used, memory_usage, elapsed_time, result[0], result[1]

# Function to save results to CSV
def save_to_csv(filename: str, pc_resources:list, fitness:list):
    with open(f"data/pc_resources/{filename}.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["CPU Time", "Memory Usage", "Elapsed Time"])  # Header
        for row in pc_resources:
            writer.writerow(row)
    
    with open(f"data/fitness/{filename}.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Average Best Fitness", "Grand Average Fitness"])
        for row in fitness:
            writer.writerow(row)

def benchmark(mh_func: GA, mh_name: str, iterations: int = 10):
    seed = [random.randint(0, 10000) for _ in range(iterations)]
    pc_resources = list()
    best_fitness = list()
    average_fitness = list()

    for i in seed:
        mh_func.setup.random.seed = i
        results = monitor_resources(lambda: mh_func.run(enable_visuals=False))
        pc_resources.append((results[0], results[1], results[2]))

        average_fitness.append(results[3])
        best_fitness.append(results[4])

    # calculating the average of i-th iteration best
    transposed = zip(*best_fitness)
    avg_best = [sum(group) / len(group) for group in transposed]

    # calculating the average of i-th iteration average
    transposed = zip(*average_fitness)
    avg_fitness = [sum(group) / len(group) for group in transposed]
    
    fitness = list(zip(avg_best, avg_fitness))
    save_to_csv(mh_name, pc_resources, fitness)


def plot_comparison(folder: str, column: str, marker: str = "o"):
    # Load the results from CSV files
    ga_data = pd.read_csv(f"{folder}/GA.csv")
    sa_data = pd.read_csv(f"{folder}/SA.csv")
    aco_data = pd.read_csv(f"{folder}/ACO.csv")

    # Plot CPU Time comparison
    plt.figure(figsize=(10, 6))

    plt.plot(range(1, len(ga_data)+1), ga_data[column], label="GA", marker=marker, color="blue")
    plt.plot(range(1, len(sa_data)+1), sa_data[column], label="SA", marker=marker, color="green")
    plt.plot(range(1, len(aco_data)+1), aco_data[column], label="ACO", marker=marker, color="red")

    plt.xlabel("Iteration", fontsize=14, fontweight="bold")
    plt.ylabel(f"{column}", fontsize=14, fontweight="bold")
    plt.title(f"{column} Comparison: GA vs SA vs ACO", fontsize=16, fontweight="bold")
    
    # Add grid with reduced opacity for better visibility
    plt.grid(True, linestyle='--', alpha=0.6)

    # Add legend with better placement
    plt.legend(loc="upper right", fontsize=12, title="Algorithms", title_fontsize=12)

    # Show the plot
    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show()

iterations = 6
benchmark(GA, "GA", iterations=iterations)
benchmark(SA, "SA", iterations=iterations)
benchmark(ACO, "ACO", iterations=iterations)

pc_resorces = "data/pc_resources"
plot_comparison(pc_resorces, "CPU Time")
plot_comparison(pc_resorces, "Memory Usage")
plot_comparison(pc_resorces, "Elapsed Time")

fitness = "data/fitness"
plot_comparison(fitness, "Average Best Fitness", marker=None)
plot_comparison(fitness, "Grand Average Fitness", marker=None)