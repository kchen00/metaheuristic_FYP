import psutil, time, csv, os, random
import GA, SA, ACO
import setup
from models.project import Project

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
    memory_usage /= 1024
    
    # Total execution time
    elapsed_time = time.time() - start_time
    
    return cpu_time_used, memory_usage, elapsed_time, result[0], result[1]

# Function to save results to CSV
def save_to_csv(mh_name: str, test_case: str, pc_resources:list, fitness:list):
    pc_resources_dir = f"data/pc_resources/{test_case}"
    fitness_dir = f"data/fitness/{test_case}"
    # check if dir ecists else create one
    if not(os.path.exists(pc_resources_dir)):
        os.makedirs(pc_resources_dir)
    if not(os.path.exists(fitness_dir)):
        os.makedirs(fitness_dir)
    
    with open(f"{pc_resources_dir}/{mh_name}.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["CPU Time", "Memory Usage", "Elapsed Time"])  # Header
        for row in pc_resources:
            writer.writerow(row)
    
    with open(f"{fitness_dir}/{mh_name}.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Average Best Fitness", "Grand Average Fitness"])
        for row in fitness:
            writer.writerow(row)

def benchmark(mh_func: GA, initial_formation: Project, mh_name: str, random_seeds: list[int]):
    pc_resources = list()
    best_fitness = list()
    average_fitness = list()

    for seed, i in enumerate(random_seeds):
        random.seed(random_seeds[seed])
        results = monitor_resources(lambda: mh_func.run(initial_formation, max_iteration=50, enable_visuals=False))
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
    save_to_csv(mh_name, initial_formation.name, pc_resources, fitness)

def plot_comparison(
    folder: str, 
    test_case: list[str], 
    column: str, 
    x_label: str,
    marker_size: int = 6, 
):
    # Read data for each algorithm
    ga_data = [pd.read_csv(f"{folder}/{test}/GA.csv") for test in test_case]
    sa_data = [pd.read_csv(f"{folder}/{test}/SA.csv") for test in test_case]
    aco_data = [pd.read_csv(f"{folder}/{test}/ACO.csv") for test in test_case]
    x = range(len(ga_data[0][column]))

    # Create a 2x2 grid of subplots
    fig, axs = plt.subplots(2, 2, figsize=(14, 12), sharex=True)
    
    # Define styles
    colors = {'GA': 'red', 'SA': 'green', 'ACO': 'blue'}
    markers = {'GA': 'o', 'SA': 's', 'ACO': 'D'}
    
    # Iterate through test cases
    for i, ax in enumerate(axs.flat):
        # Plot for each algorithm
        ax.plot(
            x, ga_data[i][column], label='GA', color=colors['GA'], 
             marker=markers['GA'], markersize=marker_size
        )
        ax.plot(
            x, sa_data[i][column], label='SA', color=colors['SA'], 
            marker=markers['SA'], markersize=marker_size
        )
        ax.plot(
            x, aco_data[i][column], label='ACO', color=colors['ACO'], 
            marker=markers['ACO'], markersize=marker_size
        )
        
        # Subplot title
        ax.set_title(f"Comparison: {test_case[i]}", fontsize=12)
        
        # Enable grid
        ax.grid(True, linestyle='--', alpha=0.6)

        # Set legend
        ax.legend(fontsize=10, loc='best')

    # Add shared axis labels
    fig.text(0.5, 0.04, x_label, ha='center', va='center', fontsize=14, fontweight='bold')
    fig.text(0.04, 0.5, column.capitalize(), ha='center', va='center', fontsize=14, fontweight='bold', rotation='vertical')
    
    # Add a shared title
    fig.suptitle(f'Algorithm Performance Comparison:  {column}', fontsize=16, fontweight='bold')

    # Adjust layout
    plt.tight_layout(rect=[0.03, 0.03, 1, 0.95])

    # Show the plot
    plt.show()

comparison = 3
random_seeds = [random.randint(1, 50) for c in range(comparison)]
for project in setup.projects:
    benchmark(GA, project, "GA", random_seeds)
    benchmark(SA, project, "SA", random_seeds)
    benchmark(ACO, project, "ACO", random_seeds)

pc_resorces = "data/pc_resources"
test_case = os.listdir(pc_resorces)
plot_comparison(pc_resorces, test_case, "CPU Time", "Comparison")
plot_comparison(pc_resorces, test_case, "Memory Usage", "Comparison")
plot_comparison(pc_resorces, test_case, "Elapsed Time", "Comparison")

fitness = "data/fitness"
test_case = os.listdir(fitness)
plot_comparison(fitness, test_case, "Average Best Fitness", "Iteration", marker_size=0)
plot_comparison(fitness, test_case, "Grand Average Fitness", "Iteration", marker_size=0)