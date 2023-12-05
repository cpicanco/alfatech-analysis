import numpy as np

def upper_summary(ax, positions, values, medians, lenghts, x=0.5, y=115, line_height=5, show_label=True):
    if show_label:
        y_pos = y
        ax.text(x, y_pos, f'N =', ha='right', color='black', fontsize=10)
        y_pos = y_pos - line_height
        ax.text(x, y_pos, f'M =', ha='right', color='black', fontsize=10)
        y_pos = y_pos - line_height
        ax.text(x, y_pos, f'Me =', ha='right', color='black', fontsize=10)
    y_pos = y
    for p, v, _len, me in zip(positions, values, lenghts, medians):
        x_pos = p
        y_pos = y
        ax.text(x_pos, y_pos, f'{_len}', ha='center', color='black', fontsize=8)
        y_pos = y_pos - line_height
        ax.text(x_pos, y_pos, f'{v:.1f}', ha='center', color='black', fontsize=8)
        y_pos = y_pos - line_height
        ax.text(x_pos, y_pos, f'{me:.1f}', ha='center', color='black', fontsize=8)

def upper_summary_2(ax, positions, lenghts, mins, maxs, x=0.5, y=115, line_height=5, show_label=True, show_n=True):
    if show_label:
        y_pos = y
        ax.text(x, y_pos, f'N =', ha='right', color='black', fontsize=10)
        y_pos = y_pos - line_height
        ax.text(x, y_pos, f'Máx =', ha='right', color='black', fontsize=10)
        y_pos = y_pos - line_height
        ax.text(x, y_pos, f'Mín =', ha='right', color='black', fontsize=10)
    first = True
    y_pos = y
    for p, _len, _max, _min in zip(positions, lenghts, maxs, mins):
        x_pos = p
        y_pos = y
        if show_n:
            ax.text(x_pos, y_pos, f'{_len}', ha='center', color='black', fontsize=8)
        else:
            if first:
                first = False
                ax.text(x_pos, y_pos, f'{_len}', ha='center', color='black', fontsize=8)

        y_pos = y_pos - line_height
        ax.text(x_pos, y_pos, f'{_max}', ha='center', color='black', fontsize=8)
        y_pos = y_pos - line_height
        ax.text(x_pos, y_pos, f'{_min}', ha='center', color='black', fontsize=8)


def default_axis_config(ax, limit_y=True):
    if limit_y:
        ax.set_ylim(-2, 102)
        ax.set_yticks(np.arange(0, 101, 20))
        ax.set_yticklabels(np.arange(0, 101, 20))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom=False, top=False)

def get_ax_top(ax):
    """
    Get the y coordinate of the top of an axes in figure coordinates

    *******MUST BE CALLED AFTER TIGHT LAYOUT******
    """
    # Create a blended transformation from data to figure coordinates
    trans = ax.transData + ax.figure.transFigure.inverted()
    # Transform the point (0, 100) from data to figure coordinates
    fig_point1 = trans.transform((0, 100))
    fig_point2 = trans.transform((0, 85))
    # Print the y-value of the figure point
    return fig_point1[1], fig_point2[1]-fig_point1[1]

def get_grouped_bar_positions(num_groups, num_items_per_group, start, gap, width):
    """Returns an array of positions for a grouped bar plot.

    Args:
        num_groups (int): The number of groups in the plot.
        num_items_per_group (int): The number of items per group.
        start (float): The starting position of the first group.
        gap (float): The gap between groups.
        width (float): The width of each bar.

    Returns:
        np.array: An array of shape (num_groups, num_items_per_group) containing the positions of each bar.

    Raises:
        ValueError: If any of the arguments are invalid.
    """
    # Validate the input arguments
    if not (isinstance(num_groups, int) and num_groups > 0):
        raise ValueError("num_groups must be a positive integer")
    if not (isinstance(num_items_per_group, int) and num_items_per_group > 0):
        raise ValueError("num_items_per_group must be a positive integer")
    if not (isinstance(start, (int, float)) and start > 0):
        raise ValueError("start must be a positive number")
    if not (isinstance(gap, (int, float)) and gap > 0):
        raise ValueError("gap must be a positive number")
    if not (isinstance(width, (int, float)) and width > 0):
        raise ValueError("width must be a positive number")

    # Create an array of group indices
    group_indices = np.arange(num_groups)
    # Create an array of item indices
    item_indices = np.arange(num_items_per_group)
    # Create a grid of group and item indices
    group_grid, item_grid = np.meshgrid(group_indices, item_indices, indexing="ij")
    # Calculate the positions of each bar using a formula
    positions = start + group_grid * (gap + 2 * width) + item_grid * (width + 0.1)
    # Return the positions array
    return positions