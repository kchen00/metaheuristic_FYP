# read Staff_Expertise_DataSet.txt from and convert it to json format
import json
import random
import matplotlib.pyplot as plt
import pandas as pd

random.seed(1)

folder = "data/staff_expertise"
# Open and read the text file
with open(f"{folder}/Staff_Expertise_DataSet.txt", "r") as file:
    lines = file.readlines()

# Create an empty dictionary to store the result
data_dict = {}

# Process each line
for line in lines:
    # Split the line into email and expertise parts
    name, expertise = line.split(" = ")

    # Clean up email and expertise
    name = name.split("@")[0]
    expertise_list = [exp.strip() for exp in expertise.split(",")]

    # Add to the dictionary
    data_dict[name] = {"expertise": expertise_list}
    data_dict[name]["salary"] = random.randint(1000, 5000)
    data_dict[name]["efficiency"] = random.random()

# add random collaboration score
for staff in data_dict:
    data_dict[staff]["scores"] = [
        random.randint(1, 5) if s != staff else 0 for s in data_dict
    ]

# save to json file
with open(f"{folder}/staff_expertise.json", "w") as f:
    json.dump(data_dict, f, indent=4)

# show member details
member_information = [[data, data_dict[name]["salary"], data_dict[name]["efficiency"], data_dict[name]["expertise"]] for data in data_dict]
data_for_df = {
    "Name": [],
    # "Salary": [],
    # "Efficiecy": [],
    "Skills": []
}

pd.set_option('display.max_colwidth', None)
for data in data_dict:
    data_for_df["Name"].append(data)
    # data_for_df["Salary"].append(data_dict[data]["salary"])
    # data_for_df["Efficiecy"].append(data_dict[data]["efficiency"])
    data_for_df["Skills"].append(data_dict[data]["expertise"])
# Create a DataFrame
df = pd.DataFrame(data_for_df)

# Pretty-print the DataFrame
print(df)

# Plot heatmap
scores = [data_dict[data]["scores"] for data in data_dict]
fig, ax = plt.subplots(figsize=(8, 6))  # Set figure size
cax = ax.imshow(scores, cmap='viridis', interpolation='nearest')
ax.set_title("Collaboration scores", fontsize=16, pad=15)
ax.grid(color='white', linestyle='-', linewidth=1.5)
cbar = fig.colorbar(cax, ax=ax, shrink=0.8, aspect=20, pad=0.02)
cbar.set_label('Score', rotation=270, labelpad=15)
plt.tight_layout()
plt.show()