import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define the data from the two dictionaries
coffee_data = {
    "additive": [1.0, 1.0],
    "name": [0.05, 0.15],
    "type": [0.0, 0.0],
    "oxidation": [0.12, 0.12],
    "caffein": [0.6666666666666666, 0.6666666666666666]
}

# Create a DataFrame
df = pd.DataFrame(coffee_data, index=['Coffee1', 'Coffee2'])

# Calculate the correlation matrix
corr_matrix = df.corr()

# Display the correlation matrix
print(corr_matrix)

sns.heatmap(corr_matrix, annot=True)
plt.show()