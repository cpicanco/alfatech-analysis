# graphication
import matplotlib.pyplot as plt
import numpy as np

def bar_plot_two_groups():
    # Data
    categories = ['Category A', 'Category B', 'Category C', 'Category D']
    group1_values = [4, 7, 2, 5]
    group2_values = [6, 3, 8, 4]

    # Set the bar width
    bar_width = 0.35

    # Calculate the positions for the bars
    bar_positions_group1 = np.arange(len(categories))
    bar_positions_group2 = bar_positions_group1 + bar_width

    # Create the bars
    plt.bar(bar_positions_group1, group1_values, width=bar_width, label='Group 1')
    plt.bar(bar_positions_group2, group2_values, width=bar_width, label='Group 2')

    # Set the labels, title, and legend
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Bar Chart with Two Groups')
    plt.xticks(bar_positions_group1 + bar_width / 2, categories)
    plt.legend()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    bar_plot_two_groups()