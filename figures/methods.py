import numpy as np

def statistics_from_block(block, key='percentages'):
    data_points = block.data[key]
    data_points = [p for p in data_points if p is not None]
    bar_length = len(data_points)
    if bar_length > 0:
        bar_value = np.mean(data_points)
        bar_std = np.std(data_points)
        bar_median = np.median(data_points)
        bar_min = np.min(data_points)
        bar_max = np.max(data_points)
    else:
        bar_value = np.nan
        bar_std = np.nan
        bar_median = np.nan
        bar_min = np.nan
        bar_max = np.nan

    return bar_value, bar_std, bar_length, bar_median, bar_min, bar_max

def statistics_from_blocks(blocks, key='percentages'):
    values, stds, lengths, medians, mins, maxs = [], [], [], [], [], []
    for block in blocks:
        value, std, length, median, min_, max_ = statistics_from_block(block, key)
        values.append(value)
        stds.append(std)
        lengths.append(length)
        medians.append(median)
        mins.append(min_)
        maxs.append(max_)
    return values, stds, lengths, medians, mins, maxs