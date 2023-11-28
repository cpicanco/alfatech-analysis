def bar_plot_two_groups():
    # graphication
    import matplotlib.pyplot as plt
    import numpy as np
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

def three_top_one_bottom():
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec

    # Create a figure and a GridSpec with 2 rows and 3 columns
    fig = plt.figure(figsize=(10, 6))
    gs = GridSpec(2, 3, height_ratios=[1, 3], width_ratios=[1, 1, 1])

    # Create three axes on the top row
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])

    # Create a larger axis at the bottom that spans all three columns
    ax_big = fig.add_subplot(gs[1, :])

    # Add content to the axes (you can customize this based on your data)
    ax1.plot([1, 2, 3], [4, 5, 6], label='Ax1')
    ax2.scatter([1, 2, 3], [4, 5, 6], label='Ax2')
    ax3.bar([1, 2, 3], [4, 5, 6], label='Ax3')
    ax_big.plot([1, 2, 3, 4, 5], [10, 8, 12, 15, 9], label='Big Ax')

    # Adjust layout and add legends if needed
    fig.tight_layout()
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax_big.legend()

    # Show the plot
    plt.show()


if __name__ == "__main__":
    bar_plot_two_groups()