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

def default_axis_config(ax, limit_y=True):
    if limit_y:
        ax.set_ylim(-2, 102)
        ax.set_yticks(np.arange(0, 101, 20))
        ax.set_yticklabels(np.arange(0, 101, 20))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(axis='x', which='both', bottom=False, top=False)
