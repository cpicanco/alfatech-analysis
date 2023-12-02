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


def multicategory_bar_chart():
    import matplotlib.pyplot as plt

    # Your data
    unid1_positions = [0, 1, 2, 3, 4]
    unid2_positions = [5, 6, 7, 8]
    unid3_positions = [9, 10, 11, 12]
    unid4_positions = [13, 14, 15, 16]
    unid5_positions = [17, 18, 19]

    # Combine positions and values
    all_positions = [unid1_positions, unid2_positions, unid3_positions, unid4_positions, unid5_positions]
    bar_values = [5, 3, 4, 7, 2, 4, 6, 8, 3, 5, 7, 2, 4, 6, 8, 3, 5, 7, 2, 4]

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Set width for the bars
    bar_width = 0.2  # Adjust this based on your preference

    # Plot the bars
    for i, positions in enumerate(all_positions):
        ax.bar([pos + i * bar_width for pos in positions], bar_values[i], width=bar_width, label=f'Unid{i+1}')

    # Add labels and legend
    ax.set_xlabel('Bar Positions')
    ax.set_ylabel('Bar Values')
    ax.legend()

    # Show the plot
    plt.show()

if __name__ == "__main__":
    multicategory_bar_chart()